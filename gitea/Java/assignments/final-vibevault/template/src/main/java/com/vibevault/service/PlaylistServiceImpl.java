package com.vibevault.service;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;
import com.vibevault.dto.SongDTO;
import com.vibevault.exception.ResourceNotFoundException;
import com.vibevault.exception.UnauthorizedException;
import com.vibevault.model.Playlist;
import com.vibevault.model.Song;
import com.vibevault.model.User;
import com.vibevault.repository.PlaylistRepository;
import com.vibevault.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 歌单服务实现
 * 
 * 需要实现：
 * - 所有 PlaylistService 接口中定义的方法
 * - 将实体转换为 DTO 返回给调用者
 * - 资源不存在时抛出 ResourceNotFoundException
 * - [Challenge] 检查用户是否有权限操作歌单（所有权检查）
 */
@Service
public class PlaylistServiceImpl implements PlaylistService {

    private final PlaylistRepository playlistRepository;
    private final UserRepository userRepository;

    public PlaylistServiceImpl(PlaylistRepository playlistRepository, UserRepository userRepository) {
        this.playlistRepository = playlistRepository;
        this.userRepository = userRepository;
    }

    @Override
    public List<PlaylistDTO> getAllPlaylists() {
        // TODO: 实现获取所有歌单
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    public PlaylistDTO getPlaylistById(Long id) {
        // TODO: 实现根据 ID 获取歌单，不存在时抛出 ResourceNotFoundException
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    @Transactional
    public PlaylistDTO createPlaylist(String name, String ownerUsername) {
        // TODO: 实现创建歌单
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    @Transactional
    public PlaylistDTO addSongToPlaylist(Long playlistId, SongCreateDTO song, String username) {
        // TODO: 实现添加歌曲到歌单
        // [Challenge] 需要检查用户是否有权限操作此歌单
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    @Transactional
    public void removeSongFromPlaylist(Long playlistId, Long songId, String username) {
        // TODO: 实现从歌单移除歌曲
        // [Challenge] 需要检查用户是否有权限操作此歌单
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    @Transactional
    public void deletePlaylist(Long playlistId, String username) {
        // TODO: 实现删除歌单
        // [Challenge] 需要检查用户是否有权限操作此歌单
        throw new UnsupportedOperationException("待实现");
    }

    // ========== Advanced 方法 ==========

    @Override
    public List<PlaylistDTO> searchPlaylists(String keyword) {
        // TODO [Advanced]: 实现按关键字搜索歌单
        throw new UnsupportedOperationException("待实现");
    }

    @Override
    @Transactional
    public PlaylistDTO copyPlaylist(Long playlistId, String newName, String username) {
        // TODO [Advanced]: 实现复制歌单
        throw new UnsupportedOperationException("待实现");
    }

    // ========== 辅助方法 ==========

    /**
     * 将 Playlist 实体转换为 DTO
     */
    private PlaylistDTO toDTO(Playlist playlist) {
        // TODO: 实现实体到 DTO 的转换
        throw new UnsupportedOperationException("待实现");
    }

    /**
     * 将 Song 实体转换为 DTO
     */
    private SongDTO toSongDTO(Song song) {
        // TODO: 实现实体到 DTO 的转换
        throw new UnsupportedOperationException("待实现");
    }

    /**
     * [Challenge] 检查用户是否有权限操作指定歌单
     * 规则：歌单所有者或管理员可以操作
     */
    private void checkPermission(Playlist playlist, String username) {
        // TODO [Challenge]: 实现权限检查
        // 如果无权限，抛出 UnauthorizedException
    }
}
