package com.vibevault.controller;

import com.vibevault.dto.PlaylistCreateDTO;
import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;
import com.vibevault.service.PlaylistService;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 歌单 REST 控制器
 * 
 * 需要实现以下端点：
 * - GET /api/playlists - 获取所有歌单（公开）
 * - GET /api/playlists/{id} - 获取指定歌单（公开）
 * - POST /api/playlists - 创建歌单（需认证）
 * - POST /api/playlists/{id}/songs - 添加歌曲（需认证）
 * - DELETE /api/playlists/{playlistId}/songs/{songId} - 移除歌曲（需认证）
 * - DELETE /api/playlists/{id} - 删除歌单（需认证）
 * 
 * [Advanced] 额外端点：
 * - GET /api/playlists/search?keyword=xxx - 搜索歌单
 * - POST /api/playlists/{id}/copy?newName=xxx - 复制歌单
 * 
 * 提示：
 * - 使用 Authentication 参数获取当前用户名：authentication.getName()
 * - 使用 @ResponseStatus 设置正确的 HTTP 状态码
 */
@RestController
@RequestMapping("/api/playlists")
public class PlaylistController {

    private final PlaylistService playlistService;

    public PlaylistController(PlaylistService playlistService) {
        this.playlistService = playlistService;
    }

    // TODO: 实现 GET /api/playlists

    // TODO: 实现 GET /api/playlists/{id}

    // TODO: 实现 POST /api/playlists (状态码 201)

    // TODO: 实现 POST /api/playlists/{id}/songs (状态码 201)

    // TODO: 实现 DELETE /api/playlists/{playlistId}/songs/{songId} (状态码 204)

    // TODO: 实现 DELETE /api/playlists/{id} (状态码 204)

    // TODO [Advanced]: 实现 GET /api/playlists/search?keyword=xxx

    // TODO [Advanced]: 实现 POST /api/playlists/{id}/copy?newName=xxx (状态码 201)
}
