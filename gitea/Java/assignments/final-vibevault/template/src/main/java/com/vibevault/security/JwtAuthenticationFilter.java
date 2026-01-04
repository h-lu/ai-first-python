package com.vibevault.security;

import com.vibevault.model.User;
import com.vibevault.repository.UserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Collections;
import java.util.List;

/**
 * JWT 认证过滤器
 * 
 * 需要实现：
 * - 从请求头中提取 Authorization: Bearer <token>
 * - 验证 token 有效性
 * - 如果有效，将用户信息设置到 SecurityContext 中
 * - [Challenge] 从数据库中读取用户角色并设置到 Authentication 中
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserRepository userRepository;

    public JwtAuthenticationFilter(JwtService jwtService, UserRepository userRepository) {
        this.jwtService = jwtService;
        this.userRepository = userRepository;
    }

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {
        
        // TODO: 实现 JWT 认证逻辑
        // 1. 从请求头获取 Authorization
        // 2. 检查是否以 "Bearer " 开头
        // 3. 提取 token 并验证
        // 4. 如果有效，创建 Authentication 并设置到 SecurityContextHolder
        // 
        // 提示：
        // - 使用 request.getHeader("Authorization") 获取头
        // - 使用 jwtService.extractUsername() 和 jwtService.isTokenValid()
        // - 使用 UsernamePasswordAuthenticationToken 创建认证对象
        // - 使用 SecurityContextHolder.getContext().setAuthentication() 设置
        
        filterChain.doFilter(request, response);
    }
}
