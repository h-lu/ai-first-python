package com.vibevault.config;

import com.vibevault.security.JwtAuthenticationFilter;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Spring Security 配置
 * 
 * 需要实现：
 * - 公开接口无需认证：/api/auth/**, GET /api/playlists, GET /api/playlists/{id}
 * - 其他接口需要认证
 * - 未认证访问受保护资源返回 401（不是 403）
 * - 配置 JWT 过滤器
 * - 禁用 CSRF（REST API 通常不需要）
 * - 使用无状态会话
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthenticationFilter) {
        this.jwtAuthenticationFilter = jwtAuthenticationFilter;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // TODO: 配置安全规则
        // 提示：
        // - 使用 http.authorizeHttpRequests() 配置路径权限
        // - 使用 http.csrf(csrf -> csrf.disable()) 禁用 CSRF
        // - 使用 http.sessionManagement() 配置无状态会话
        // - 使用 http.exceptionHandling() 配置 401 响应
        // - 使用 http.addFilterBefore() 添加 JWT 过滤器
        
        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
