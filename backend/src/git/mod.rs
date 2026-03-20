// Git 自动化模块
// 负责 Git 分支管理、自动提交和推送等操作

use git2::{Repository, StatusOptions, BranchType};
use std::path::{Path, PathBuf};
use std::process::Command;
use thiserror::Error;

/// Git 操作错误类型
#[derive(Debug, Error)]
pub enum GitError {
    #[error("Git 仓库错误: {0}")]
    RepositoryError(#[from] git2::Error),
    
    #[error("工作区不干净，存在未提交的更改")]
    DirtyWorkingTree,
    
    #[error("分支 {0} 不存在")]
    BranchNotFound(String),
    
    #[error("分支 {0} 已存在")]
    BranchAlreadyExists(String),
    
    #[error("无法找到 Git 仓库")]
    RepoNotFound,
    
    #[error("操作失败: {0}")]
    OperationFailed(String),
    
    #[error("代码验证失败: {0}")]
    ValidationFailed(String),
    
    #[error("命令执行失败: {0}")]
    CommandFailed(String),
    
    #[error("远程仓库 {0} 不存在")]
    RemoteNotFound(String),
}

/// Git 自动化管理器
/// 
/// 提供 Git 仓库的自动化操作功能，包括：
/// - 工作区状态验证
/// - 分支创建和管理
/// - 标签创建和管理
/// - 远程推送操作
pub struct GitAutomation {
    /// Git 仓库路径
    repo_path: PathBuf,
}

/// 分支操作配置
pub struct BranchOperation {
    /// 源分支名称
    pub source_branch: String,
    /// 目标分支名称
    pub target_branch: String,
    /// 备份标签名称
    pub backup_tag: String,
}

/// 提交类型枚举
#[derive(Debug, Clone, Copy)]
pub enum CommitType {
    /// 新增功能
    Feat,
    /// 修复 Bug
    Fix,
    /// 性能优化
    Perf,
    /// 构建配置/依赖更新
    Chore,
}

impl CommitType {
    /// 转换为字符串标签
    pub fn as_str(&self) -> &'static str {
        match self {
            CommitType::Feat => "feat",
            CommitType::Fix => "fix",
            CommitType::Perf => "perf",
            CommitType::Chore => "chore",
        }
    }
}

/// 提交配置
pub struct CommitConfig {
    /// 提交类型
    pub commit_type: CommitType,
    /// 功能描述
    pub description: String,
    /// 细节说明（可选）
    pub details: Option<String>,
}

impl GitAutomation {
    /// 创建新的 Git 自动化管理器
    ///
    /// # 参数
    /// * `repo_path` - Git 仓库路径
    ///
    /// # 返回
    /// * `Result<Self, GitError>` - 成功返回 GitAutomation 实例，失败返回错误
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// ```
    pub fn new<P: AsRef<Path>>(repo_path: P) -> Result<Self, GitError> {
        let repo_path = repo_path.as_ref().to_path_buf();
        
        // 验证路径是否为有效的 Git 仓库
        Repository::open(&repo_path)?;
        
        Ok(Self { repo_path })
    }
    
    /// 验证工作区是否干净（无未提交的更改）
    ///
    /// 这是任务 1.1 要求的核心方法之一。
    /// 在执行任何 Git 操作前，必须先验证工作区状态。
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 工作区干净返回 Ok(())，否则返回 DirtyWorkingTree 错误
    ///
    /// # 错误
    /// * `GitError::DirtyWorkingTree` - 工作区存在未提交的更改
    /// * `GitError::RepositoryError` - Git 仓库操作失败
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// git.verify_clean_working_tree()?;
    /// println!("工作区干净，可以继续操作");
    /// ```
    pub fn verify_clean_working_tree(&self) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取工作区状态
        let mut opts = StatusOptions::new();
        opts.include_untracked(true);
        opts.include_ignored(false);
        
        let statuses = repo.statuses(Some(&mut opts))?;
        
        // 如果状态列表不为空，说明有未提交的更改
        if !statuses.is_empty() {
            log::warn!("工作区不干净，存在 {} 个未提交的更改", statuses.len());
            return Err(GitError::DirtyWorkingTree);
        }
        
        log::info!("工作区验证通过：无未提交更改");
        Ok(())
    }
    
    /// 检查工作区是否干净（无未提交的更改）
    ///
    /// 这是 verify_clean_working_tree 的布尔值版本，用于条件判断。
    ///
    /// # 返回
    /// * `Result<bool, GitError>` - true 表示工作区干净，false 表示有未提交更改
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// if git.check_working_tree_clean()? {
    ///     println!("工作区干净");
    /// }
    /// ```
    pub fn check_working_tree_clean(&self) -> Result<bool, GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取工作区状态
        let mut opts = StatusOptions::new();
        opts.include_untracked(true);
        opts.include_ignored(false);
        
        let statuses = repo.statuses(Some(&mut opts))?;
        
        // 如果状态列表为空，说明工作区干净
        Ok(statuses.is_empty())
    }
    
    /// 创建新分支
    ///
    /// 这是任务 1.1 要求的核心方法之一。
    /// 从当前 HEAD 创建新分支，但不切换到新分支。
    ///
    /// # 参数
    /// * `branch_name` - 新分支的名称
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 Ok(())，失败返回错误
    ///
    /// # 错误
    /// * `GitError::BranchAlreadyExists` - 分支已存在
    /// * `GitError::RepositoryError` - Git 仓库操作失败
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// git.create_branch("feature/new-feature")?;
    /// println!("分支创建成功");
    /// ```
    pub fn create_branch(&self, branch_name: &str) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 检查分支是否已存在
        if repo.find_branch(branch_name, BranchType::Local).is_ok() {
            log::warn!("分支 {} 已存在", branch_name);
            return Err(GitError::BranchAlreadyExists(branch_name.to_string()));
        }
        
        // 获取当前 HEAD 的 commit
        let head = repo.head()?;
        let commit = head.peel_to_commit()?;
        
        // 创建新分支（不切换）
        repo.branch(branch_name, &commit, false)?;
        
        log::info!("成功创建分支: {}", branch_name);
        Ok(())
    }
    
    /// 添加 Git 标签
    ///
    /// 这是任务 1.1 要求的核心方法之一。
    /// 在当前 HEAD 创建带注释的标签。
    ///
    /// # 参数
    /// * `tag_name` - 标签名称
    /// * `message` - 标签注释信息
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 Ok(())，失败返回错误
    ///
    /// # 错误
    /// * `GitError::RepositoryError` - Git 仓库操作失败
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// git.add_tag("v1.0.0-archived", "归档 v1 版本")?;
    /// println!("标签创建成功");
    /// ```
    pub fn add_tag(&self, tag_name: &str, message: &str) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取当前 HEAD 的 commit
        let head = repo.head()?;
        let commit = head.peel_to_commit()?;
        
        // 获取签名信息
        let signature = repo.signature()?;
        
        // 创建带注释的标签
        repo.tag(
            tag_name,
            commit.as_object(),
            &signature,
            message,
            false, // 不覆盖已存在的标签
        )?;
        
        log::info!("成功创建标签: {} ({})", tag_name, message);
        Ok(())
    }
    
    /// 推送到远程仓库
    ///
    /// 这是任务 1.1 要求的核心方法之一。
    /// 推送指定分支和可选的标签到远程仓库。
    ///
    /// # 参数
    /// * `branch` - 要推送的分支名称
    /// * `tags` - 是否同时推送标签
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 Ok(())，失败返回错误
    ///
    /// # 错误
    /// * `GitError::BranchNotFound` - 分支不存在
    /// * `GitError::RemoteNotFound` - 远程仓库不存在
    /// * `GitError::RepositoryError` - Git 仓库操作失败
    ///
    /// # 示例
    /// ```
    /// let git = GitAutomation::new(".")?;
    /// // 推送分支和标签
    /// git.push_to_remote("main", true)?;
    /// println!("推送成功");
    /// ```
    pub fn push_to_remote(&self, branch: &str, tags: bool) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 验证分支是否存在
        repo.find_branch(branch, BranchType::Local)
            .map_err(|_| GitError::BranchNotFound(branch.to_string()))?;
        
        // 获取远程仓库（默认为 origin）
        let mut remote = repo.find_remote("origin")
            .map_err(|_| GitError::RemoteNotFound("origin".to_string()))?;
        
        // 构建推送引用规范
        let mut refspecs = vec![format!("refs/heads/{}:refs/heads/{}", branch, branch)];
        
        // 如果需要推送标签，添加标签引用规范
        if tags {
            refspecs.push("refs/tags/*:refs/tags/*".to_string());
        }
        
        // 执行推送
        let mut push_options = git2::PushOptions::new();
        remote.push(&refspecs, Some(&mut push_options))?;
        
        if tags {
            log::info!("成功推送分支 {} 和所有标签到远程仓库", branch);
        } else {
            log::info!("成功推送分支 {} 到远程仓库", branch);
        }
        
        Ok(())
    }
    
    /// 创建备份标签（轻量级标签）
    ///
    /// # 参数
    /// * `tag_name` - 标签名称
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    pub fn create_backup_tag(&self, tag_name: &str) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取当前 HEAD 的 commit
        let head = repo.head()?;
        let commit = head.peel_to_commit()?;
        
        // 创建轻量级标签
        repo.tag_lightweight(tag_name, commit.as_object(), false)?;
        
        log::info!("创建备份标签: {}", tag_name);
        Ok(())
    }
    
    /// 强制重置分支到指定目标
    ///
    /// # 参数
    /// * `branch` - 要重置的分支名称
    /// * `target` - 目标分支或 commit
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    pub fn force_reset_branch(&self, branch: &str, target: &str) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 查找目标分支的 commit
        let target_ref = repo.find_reference(&format!("refs/heads/{}", target))?;
        let target_commit = target_ref.peel_to_commit()?;
        
        // 切换到要重置的分支
        let branch_ref = repo.find_reference(&format!("refs/heads/{}", branch))?;
        repo.set_head(branch_ref.name().ok_or_else(|| {
            GitError::OperationFailed("无法获取分支引用名称".to_string())
        })?)?;
        
        // 强制重置到目标 commit
        repo.reset(
            target_commit.as_object(),
            git2::ResetType::Hard,
            None,
        )?;
        
        log::info!("分支 {} 已强制重置到 {}", branch, target);
        Ok(())
    }
    
    /// 推送所有分支到远程仓库
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    pub fn push_all_branches(&self) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取远程仓库（默认为 origin）
        let mut remote = repo.find_remote("origin")?;
        
        // 获取所有本地分支
        let branches = repo.branches(Some(git2::BranchType::Local))?;
        let mut refspecs = Vec::new();
        
        for branch_result in branches {
            let (branch, _) = branch_result?;
            if let Some(name) = branch.name()? {
                refspecs.push(format!("refs/heads/{}:refs/heads/{}", name, name));
            }
        }
        
        // 推送所有分支（使用 force）
        let mut push_options = git2::PushOptions::new();
        remote.push(
            &refspecs.iter().map(|s| format!("+{}", s)).collect::<Vec<_>>(),
            Some(&mut push_options),
        )?;
        
        // 推送所有标签
        remote.push(&["+refs/tags/*:refs/tags/*"], Some(&mut push_options))?;
        
        log::info!("已推送所有分支和标签到远程仓库");
        Ok(())
    }
    
    /// 回滚操作（恢复到备份标签）
    ///
    /// # 参数
    /// * `backup_tag` - 备份标签名称
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    pub fn rollback(&self, backup_tag: &str) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 查找备份标签
        let tag_ref = repo.find_reference(&format!("refs/tags/{}", backup_tag))?;
        let commit = tag_ref.peel_to_commit()?;
        
        // 重置到备份点
        repo.reset(commit.as_object(), git2::ResetType::Hard, None)?;
        
        log::info!("已回滚到备份标签: {}", backup_tag);
        Ok(())
    }
    
    /// 执行分支迁移操作
    ///
    /// # 参数
    /// * `operation` - 分支操作配置
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    ///
    /// # 流程
    /// 1. 验证工作区干净
    /// 2. 创建备份标签
    /// 3. 创建 flet 分支保存当前 master
    /// 4. 强制重置 master 到 tauri-v3
    /// 5. 推送所有分支
    pub fn migrate_branches(&self, operation: BranchOperation) -> Result<(), GitError> {
        // 1. 验证工作区干净
        self.verify_clean_working_tree()?;
        
        let repo = Repository::open(&self.repo_path)?;
        
        // 2. 创建备份标签
        self.create_backup_tag(&operation.backup_tag)?;
        
        // 3. 创建 flet 分支保存当前 master
        let master_ref = repo.find_reference(&format!("refs/heads/{}", operation.target_branch))?;
        let master_commit = master_ref.peel_to_commit()?;
        repo.branch("flet", &master_commit, false)?;
        log::info!("创建 flet 分支保存当前 master");
        
        // 4. 强制重置 master 到 tauri-v3
        self.force_reset_branch(&operation.target_branch, &operation.source_branch)?;
        
        // 5. 推送所有分支
        self.push_all_branches()?;
        
        log::info!("分支迁移完成");
        Ok(())
    }
    
    /// 生成提交信息
    ///
    /// # 参数
    /// * `config` - 提交配置
    ///
    /// # 返回
    /// * `String` - 格式化的提交信息
    ///
    /// # 格式
    /// `[类型] 功能描述 - 细节说明`
    ///
    /// # 示例
    /// ```
    /// let config = CommitConfig {
    ///     commit_type: CommitType::Feat,
    ///     description: "实现服务管理器".to_string(),
    ///     details: Some("支持多实例并发管理".to_string()),
    /// };
    /// let message = GitAutomation::generate_commit_message(&config);
    /// // 结果: "[feat] 实现服务管理器 - 支持多实例并发管理"
    /// ```
    pub fn generate_commit_message(config: &CommitConfig) -> String {
        if let Some(details) = &config.details {
            format!("[{}] {} - {}", config.commit_type.as_str(), config.description, details)
        } else {
            format!("[{}] {}", config.commit_type.as_str(), config.description)
        }
    }
    
    /// 执行代码验证（cargo check 和 npm run lint）
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 验证通过返回 ()，失败返回错误
    pub fn validate_code(&self) -> Result<(), GitError> {
        log::info!("开始代码验证...");
        
        // 1. 执行 cargo check
        log::info!("执行 cargo check...");
        let cargo_output = Command::new("cargo")
            .arg("check")
            .current_dir(self.repo_path.join("prism-local-server-tauri/src-tauri"))
            .output()
            .map_err(|e| GitError::CommandFailed(format!("无法执行 cargo check: {}", e)))?;
        
        if !cargo_output.status.success() {
            let stderr = String::from_utf8_lossy(&cargo_output.stderr);
            return Err(GitError::ValidationFailed(format!(
                "cargo check 失败:\n{}",
                stderr
            )));
        }
        log::info!("cargo check 通过");
        
        // 2. 执行 npm run lint
        log::info!("执行 npm run lint...");
        let npm_output = Command::new("npm")
            .args(&["run", "lint"])
            .current_dir(self.repo_path.join("prism-local-server-tauri"))
            .output()
            .map_err(|e| GitError::CommandFailed(format!("无法执行 npm run lint: {}", e)))?;
        
        if !npm_output.status.success() {
            let stderr = String::from_utf8_lossy(&npm_output.stderr);
            return Err(GitError::ValidationFailed(format!(
                "npm run lint 失败:\n{}",
                stderr
            )));
        }
        log::info!("npm run lint 通过");
        
        log::info!("代码验证完成");
        Ok(())
    }
    
    /// 自动提交并推送
    ///
    /// # 参数
    /// * `config` - 提交配置
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    ///
    /// # 流程
    /// 1. 执行代码验证（cargo check + npm run lint）
    /// 2. 检查是否有更改需要提交
    /// 3. 生成提交信息
    /// 4. 提交所有更改
    /// 5. 推送到远程仓库
    pub fn auto_commit_and_push(&self, config: CommitConfig) -> Result<(), GitError> {
        // 1. 执行代码验证
        self.validate_code()?;
        
        let repo = Repository::open(&self.repo_path)?;
        
        // 2. 检查是否有更改
        let mut status_opts = StatusOptions::new();
        status_opts.include_untracked(true);
        status_opts.include_ignored(false);
        
        let statuses = repo.statuses(Some(&mut status_opts))?;
        if statuses.is_empty() {
            log::info!("没有需要提交的更改");
            return Ok(());
        }
        
        // 3. 生成提交信息
        let message = Self::generate_commit_message(&config);
        log::info!("提交信息: {}", message);
        
        // 4. 添加所有更改到暂存区
        let mut index = repo.index()?;
        index.add_all(["*"].iter(), git2::IndexAddOption::DEFAULT, None)?;
        index.write()?;
        
        // 5. 创建提交
        let tree_id = index.write_tree()?;
        let tree = repo.find_tree(tree_id)?;
        let signature = repo.signature()?;
        let parent_commit = repo.head()?.peel_to_commit()?;
        
        repo.commit(
            Some("HEAD"),
            &signature,
            &signature,
            &message,
            &tree,
            &[&parent_commit],
        )?;
        
        log::info!("提交成功");
        
        // 6. 推送到远程仓库
        self.push_current_branch()?;
        
        log::info!("推送成功");
        Ok(())
    }
    
    /// 推送当前分支到远程仓库
    ///
    /// # 返回
    /// * `Result<(), GitError>` - 成功返回 ()，失败返回错误
    fn push_current_branch(&self) -> Result<(), GitError> {
        let repo = Repository::open(&self.repo_path)?;
        
        // 获取当前分支名称
        let head = repo.head()?;
        let branch_name = head
            .shorthand()
            .ok_or_else(|| GitError::OperationFailed("无法获取当前分支名称".to_string()))?;
        
        // 获取远程仓库
        let mut remote = repo.find_remote("origin")?;
        
        // 推送当前分支
        let refspec = format!("refs/heads/{}:refs/heads/{}", branch_name, branch_name);
        let mut push_options = git2::PushOptions::new();
        remote.push(&[&refspec], Some(&mut push_options))?;
        
        log::info!("已推送分支 {} 到远程仓库", branch_name);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    
    /// 测试工作区状态检查
    #[test]
    fn test_check_working_tree_clean() {
        // 注意：这个测试需要在实际的 Git 仓库中运行
        // 在 CI 环境中可能需要跳过
        if let Ok(current_dir) = env::current_dir() {
            if let Ok(git) = GitAutomation::new(&current_dir) {
                // 只是验证方法可以调用，不验证具体结果
                let _ = git.check_working_tree_clean();
            }
        }
    }
    
    /// 测试验证工作区方法
    #[test]
    fn test_verify_clean_working_tree() {
        if let Ok(current_dir) = env::current_dir() {
            if let Ok(git) = GitAutomation::new(&current_dir) {
                // 验证方法可以调用
                let _ = git.verify_clean_working_tree();
            }
        }
    }
    
    /// 测试无效路径
    #[test]
    fn test_new_with_invalid_path() {
        // 测试无效路径
        let result = GitAutomation::new("/nonexistent/path");
        assert!(result.is_err());
    }
    
    /// 测试提交类型转换
    #[test]
    fn test_commit_type_as_str() {
        assert_eq!(CommitType::Feat.as_str(), "feat");
        assert_eq!(CommitType::Fix.as_str(), "fix");
        assert_eq!(CommitType::Perf.as_str(), "perf");
        assert_eq!(CommitType::Chore.as_str(), "chore");
    }
    
    /// 测试提交信息生成
    #[test]
    fn test_generate_commit_message() {
        let config = CommitConfig {
            commit_type: CommitType::Feat,
            description: "实现 Git 自动化模块".to_string(),
            details: Some("添加分支创建和标签管理功能".to_string()),
        };
        
        let message = GitAutomation::generate_commit_message(&config);
        assert_eq!(message, "[feat] 实现 Git 自动化模块 - 添加分支创建和标签管理功能");
        
        let config_no_details = CommitConfig {
            commit_type: CommitType::Fix,
            description: "修复工作区验证问题".to_string(),
            details: None,
        };
        
        let message_no_details = GitAutomation::generate_commit_message(&config_no_details);
        assert_eq!(message_no_details, "[fix] 修复工作区验证问题");
    }
}
