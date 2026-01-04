package com.vibevault.model;

import jakarta.persistence.*;

/**
 * 用户实体类
 * 
 * 需要实现：
 * - 将此类映射为数据库表 "users"
 * - id 作为自增主键
 * - username 必须唯一且不能为空
 * - password 不能为空
 * - [Challenge] 支持用户角色（如 ROLE_USER, ROLE_ADMIN）
 */
public class User {

    private Long id;

    private String username;

    private String password;

    // [Challenge] 用户角色，默认为 ROLE_USER
    private String role = "ROLE_USER";

    protected User() {
    }

    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public User(String username, String password, String role) {
        this.username = username;
        this.password = password;
        this.role = role;
    }

    public Long getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
}
