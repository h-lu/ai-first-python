package com.vibevault.repository;

import com.vibevault.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 用户仓库接口
 * 
 * 需要实现：
 * - 根据用户名查找用户
 * - 检查用户名是否已存在
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // TODO: 添加必要的查询方法
}
