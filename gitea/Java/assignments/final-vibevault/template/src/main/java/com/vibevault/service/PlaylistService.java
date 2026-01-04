package com.vibevault.service;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;

import java.util.List;

/**
 * 歌单服务接口
 * 定义歌单相关的业务操作
 */
public interface PlaylistService {

    /**
     * 获取所有歌单
     */
    List<PlaylistDTO> getAllPlaylists();

    /**
     * 根据 ID 获取歌单
     * @throws com.vibevault.exception.ResourceNotFoundException 如果歌单不存在
     */
    PlaylistDTO getPlaylistById(Long id);

    /**
     * 创建新歌单
     * @param name 歌单名称
     * @param ownerUsername 所有者用户名
     */
    PlaylistDTO createPlaylist(String name, String ownerUsername);

    /**
     * 向歌单添加歌曲
     * @param playlistId 歌单 ID
     * @param song 歌曲信息
     * @param username 当前用户名（用于权限检查）
     */
    PlaylistDTO addSongToPlaylist(Long playlistId, SongCreateDTO song, String username);

    /**
     * 从歌单移除歌曲
     * @param playlistId 歌单 ID
     * @param songId 歌曲 ID
     * @param username 当前用户名（用于权限检查）
     */
    void removeSongFromPlaylist(Long playlistId, Long songId, String username);

    /**
     * 删除歌单
     * @param playlistId 歌单 ID
     * @param username 当前用户名（用于权限检查）
     */
    void deletePlaylist(Long playlistId, String username);

    // ========== Advanced 方法（选做）==========

    /**
     * [Advanced] 按关键字搜索歌单
     */
    List<PlaylistDTO> searchPlaylists(String keyword);

    /**
     * [Advanced] 复制歌单
     */
    PlaylistDTO copyPlaylist(Long playlistId, String newName, String username);
}
