package com.vibevault.security;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT 服务
 * 
 * 需要实现：
 * - 生成 JWT token（包含用户名）
 * - 从 token 中提取用户名
 * - 验证 token 是否有效（未过期、签名正确）
 */
@Service
public class JwtService {

    @Value("${jwt.secret:your-secret-key-here-should-be-at-least-256-bits-long-for-hs256}")
    private String secret;

    @Value("${jwt.expiration:86400000}")
    private long expiration;

    /**
     * 为用户生成 JWT token
     */
    public String generateToken(String username) {
        // TODO: 实现 token 生成
        // 提示：使用 Jwts.builder()
        throw new UnsupportedOperationException("待实现");
    }

    /**
     * 从 token 中提取用户名
     */
    public String extractUsername(String token) {
        // TODO: 实现用户名提取
        // 提示：使用 Jwts.parser()
        throw new UnsupportedOperationException("待实现");
    }

    /**
     * 验证 token 是否有效
     */
    public boolean isTokenValid(String token, String username) {
        // TODO: 实现 token 验证
        throw new UnsupportedOperationException("待实现");
    }

    /**
     * 获取签名密钥
     */
    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
    }
}
