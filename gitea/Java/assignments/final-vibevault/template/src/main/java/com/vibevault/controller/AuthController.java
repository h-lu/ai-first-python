package com.vibevault.controller;

import com.vibevault.model.User;
import com.vibevault.repository.UserRepository;
import com.vibevault.security.JwtService;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

/**
 * 认证控制器
 * 
 * 需要实现以下端点：
 * - POST /api/auth/register - 用户注册
 *   - 检查用户名是否已存在（已存在返回 409 Conflict）
 *   - 密码需要加密存储
 *   - 成功返回 201
 * 
 * - POST /api/auth/login - 用户登录
 *   - 验证用户名和密码
 *   - 验证失败返回 401 Unauthorized
 *   - 验证成功返回 JWT token
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthController(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    // TODO: 实现 POST /api/auth/register (状态码 201)

    // TODO: 实现 POST /api/auth/login
}

/**
 * 注册请求 DTO
 */
record RegisterRequest(String username, String password) {}

/**
 * 注册响应 DTO
 */
record RegisterResponse(String message, String username) {}

/**
 * 登录请求 DTO
 */
record LoginRequest(String username, String password) {}

/**
 * 登录响应 DTO
 */
record LoginResponse(String token, String username) {}
