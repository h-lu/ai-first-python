package com.vibevault.repository;

import com.vibevault.model.Playlist;
import com.vibevault.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 歌单仓库接口
 * 
 * 基础功能由 JpaRepository 提供
 * 
 * [Advanced] 需要添加：
 * - 按所有者查询歌单
 * - 按名称模糊搜索歌单
 */
@Repository
public interface PlaylistRepository extends JpaRepository<Playlist, Long> {
    // TODO [Advanced]: 添加高级查询方法
}
