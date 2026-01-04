# VibeVault 期末大作业

本大作业要求你在给定的起始代码基础上，完成一个**可运行、可测试、可说明**的 VibeVault 后端系统。

---

## 一、学习目标

- **掌握端到端后端工程能力**：从实体建模、REST API 设计到数据库与事务管理
- **应用三层架构与设计原则**：通过 Controller / Service / Repository 分层
- **构建自动化测试安全网**：使用 JUnit/AssertJ 等工具为核心业务编写测试
- **理解并实现基础安全机制**：落地最小可用的认证与授权骨架
- **学会与 AI 协同开发**：通过高质量 Prompt 使用大模型辅助开发

---

## 二、运行环境

- **JDK 21**
- **Gradle**（使用仓库内 Wrapper：`./gradlew`）
- **Spring Boot 3.4.x**

**本地常用命令**：
```bash
./gradlew test      # 编译与测试
./gradlew bootRun   # 运行应用
```

---

## 三、功能要求

### 🟢 Core 轨道（必做，约 60 分）

#### 1. 实体层（model 包）

完善 `User`、`Playlist`、`Song` 三个 JPA 实体类：

- **User**：用户实体，映射到 `users` 表
  - 用户名必须唯一且不能为空
  - 密码不能为空
  - 包含角色字段（默认 `ROLE_USER`）

- **Playlist**：歌单实体，映射到 `playlists` 表
  - 每个歌单属于一个用户（多对一）
  - 一个歌单包含多首歌曲（一对多）
  - 删除歌单时应级联删除其中的歌曲
  - 实现 `addSong()` 和 `removeSong()` 方法维护双向关系

- **Song**：歌曲实体，映射到 `songs` 表
  - 每首歌曲属于一个歌单（多对一）

#### 2. 仓库层（repository 包）

- **UserRepository**：提供根据用户名查找用户、检查用户名是否存在的方法
- **PlaylistRepository**：继承 JpaRepository 即可

#### 3. 服务层（service 包）

实现 `PlaylistServiceImpl` 中的所有方法：

- 获取所有歌单
- 根据 ID 获取歌单（不存在时抛出 `ResourceNotFoundException`）
- 创建新歌单
- 向歌单添加歌曲
- 从歌单移除歌曲
- 删除歌单

#### 4. 控制器层（controller 包）

**PlaylistController** - 歌单 REST API：

| 端点 | 说明 | 状态码 |
|------|------|--------|
| `GET /api/playlists` | 获取所有歌单 | 200 |
| `GET /api/playlists/{id}` | 获取指定歌单 | 200 / 404 |
| `POST /api/playlists` | 创建新歌单 | 201 |
| `POST /api/playlists/{id}/songs` | 添加歌曲 | 201 |
| `DELETE /api/playlists/{playlistId}/songs/{songId}` | 移除歌曲 | 204 |
| `DELETE /api/playlists/{id}` | 删除歌单 | 204 |

**AuthController** - 认证 API：

| 端点 | 说明 | 状态码 |
|------|------|--------|
| `POST /api/auth/register` | 用户注册 | 201 / 409（用户名已存在） |
| `POST /api/auth/login` | 用户登录 | 200（返回 JWT）/ 401 |

#### 5. 安全配置（security 和 config 包）

- 配置公开接口：`/api/auth/**`、`GET /api/playlists`、`GET /api/playlists/{id}`
- 其他接口需要认证
- 未认证访问受保护资源返回 **401 Unauthorized**
- 实现 JWT 生成、验证和过滤器

---

### 🟡 Advanced 轨道（进阶，约 10 分）

#### 1. 事务与一致性

- 确保 Service 层的写操作都有事务支持
- 批量操作保证原子性

#### 2. 高级查询

在 Repository 和 Service 层添加：

- 按所有者查询歌单
- 按名称模糊搜索歌单
- 复制歌单功能

对应的 Controller 端点：

| 端点 | 说明 |
|------|------|
| `GET /api/playlists/search?keyword=xxx` | 搜索歌单 |
| `POST /api/playlists/{id}/copy?newName=xxx` | 复制歌单 |

#### 3. 统一异常处理

使用 `@RestControllerAdvice` 实现全局异常处理：

- `ResourceNotFoundException` → 404
- `UnauthorizedException` → 403
- 其他异常 → 合适的状态码

---

### 🔴 Challenge 轨道（挑战，约 10 分）

#### 1. 所有权检查

- 只有歌单所有者可以修改/删除自己的歌单
- 非所有者操作他人歌单返回 **403 Forbidden**

#### 2. 角色权限

- 支持用户角色（`ROLE_USER`、`ROLE_ADMIN`）
- 管理员可以删除任何用户的歌单
- 普通用户只能删除自己的歌单

---

## 四、报告要求（约 20 分）

> 📝 **写作指导**：请参考 `REPORT_GUIDE.md` 和 `FRONTEND_GUIDE.md` 了解详细的写作要求和格式说明。

### REPORT.md - 后端开发反思报告（10 分）

在 `REPORT.md` 文件中撰写后端开发反思报告，建议 **800–1500 字**，围绕以下三个问题展开：

1. **问题解决（4 分）**：你遇到的最大挑战是什么？你是如何解决的？
2. **反思深度（3 分）**：如果重新做一遍，你会有什么不同的设计决策？
3. **AI 使用（3 分）**：你如何使用 AI 辅助开发？有什么经验教训？

> ⚠️ 我们想听到的是**你的思考**，而非代码的复述。

### FRONTEND.md - 前端开发反思报告（10 分）

在 `FRONTEND.md` 文件中撰写前端开发反思报告，建议 **600–1200 字**，围绕以下三个问题展开：

1. **界面展示（5 分）**：提供 3–6 张截图展示你的界面，每张配简要说明
2. **问题解决（3 分）**：你在前端开发中遇到的最大挑战是什么？
3. **反思改进（2 分）**：如果重新做一遍，你会如何改进？

> 📁 **截图位置**：将截图保存到仓库根目录下的 `images/` 文件夹

---

## 五、评分构成

| 项目 | 分值 | 说明 |
|------|------|------|
| Core 测试 | 60 分 | 实体、Service、Controller、基础安全 |
| Advanced 测试 | 10 分 | 事务、高级查询、统一异常处理 |
| Challenge 测试 | 10 分 | 所有权检查、角色权限 |
| REPORT.md | 10 分 | LLM 自动评分 |
| FRONTEND.md | 10 分 | LLM 自动评分 |

> ⚠️ **通过本地公开测试 ≠ 拿满分**。隐藏测试会检查更多边界条件。

---

## 六、提交流程

1. 克隆仓库到本地
2. 完成代码开发
3. 运行 `./gradlew test` 确保公开测试通过
4. 完成 `REPORT.md` 和 `FRONTEND.md`
5. `git add / commit / push` 到 `main` 分支
6. **触发自动评分**（二选一）：
   - 在 commit message 中包含 **"完成作业"** 字样
   - 或推送 `submit` 开头的标签：`git tag submit && git push origin submit`
7. 在 Gitea Actions 页面查看评分结果

> 💡 **提示**：普通提交不会触发自动评分，这样你可以在开发过程中自由提交而不用担心消耗评分次数。

---

## 七、学术诚信

- ❌ 禁止直接复制他人代码或报告
- ✅ 允许使用 AI 辅助，但必须**完全理解**生成的代码
- ⚠️ 教师可能通过口头问答或现场演示抽查

---

## 八、建议节奏

- **第 1 周**：完成实体建模（JPA 注解）、Repository、Playlist.addSong/removeSong
- **第 2 周**：完成 Service 层、Controller 层、认证接口
- **第 3 周**：完成 Security 配置、Advanced 和 Challenge 任务
- **截止前**：完成报告，最后一轮自测

---

## 九、代码结构说明

```
src/main/java/com/vibevault/
├── VibeVaultApplication.java    # 启动类（已完成）
├── config/
│   └── SecurityConfig.java      # 安全配置（待实现）
├── controller/
│   ├── AuthController.java      # 认证控制器（待实现）
│   └── PlaylistController.java  # 歌单控制器（待实现）
├── dto/
│   ├── PlaylistDTO.java         # 歌单响应 DTO（已完成）
│   ├── PlaylistCreateDTO.java   # 创建歌单请求 DTO（已完成）
│   ├── SongDTO.java             # 歌曲响应 DTO（已完成）
│   └── SongCreateDTO.java       # 添加歌曲请求 DTO（已完成）
├── exception/
│   ├── GlobalExceptionHandler.java    # 全局异常处理（待实现）
│   ├── ResourceNotFoundException.java # 资源不存在异常（已完成）
│   └── UnauthorizedException.java     # 未授权异常（已完成）
├── model/
│   ├── User.java                # 用户实体（待添加 JPA 注解）
│   ├── Playlist.java            # 歌单实体（待添加 JPA 注解）
│   └── Song.java                # 歌曲实体（待添加 JPA 注解）
├── repository/
│   ├── UserRepository.java      # 用户仓库（待添加查询方法）
│   └── PlaylistRepository.java  # 歌单仓库（待添加查询方法）
├── security/
│   ├── JwtService.java          # JWT 服务（待实现）
│   └── JwtAuthenticationFilter.java  # JWT 过滤器（待实现）
└── service/
    ├── PlaylistService.java     # 歌单服务接口（已完成）
    └── PlaylistServiceImpl.java # 歌单服务实现（待实现）
```

祝你顺利完成！记住：**理解永远比"跑通一次"更重要。**
