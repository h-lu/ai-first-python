package com.vibevault.core;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vibevault.dto.PlaylistCreateDTO;
import com.vibevault.model.Playlist;
import com.vibevault.model.User;
import com.vibevault.repository.PlaylistRepository;
import com.vibevault.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Core 轨道测试：REST API 端点
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class CoreControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = userRepository.save(new User("testuser", passwordEncoder.encode("password")));
    }

    @Test
    @DisplayName("GET /api/playlists 应该返回所有歌单")
    void getAllPlaylists_shouldReturnPlaylists() throws Exception {
        playlistRepository.save(new Playlist("Playlist 1", testUser));
        playlistRepository.save(new Playlist("Playlist 2", testUser));

        mockMvc.perform(get("/api/playlists"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(2));
    }

    @Test
    @DisplayName("GET /api/playlists/{id} 应该返回指定歌单")
    void getPlaylist_shouldReturnPlaylist() throws Exception {
        Playlist playlist = playlistRepository.save(new Playlist("Test Playlist", testUser));

        mockMvc.perform(get("/api/playlists/" + playlist.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Playlist"))
                .andExpect(jsonPath("$.ownerUsername").value("testuser"));
    }

    @Test
    @DisplayName("GET /api/playlists/{id} 对于不存在的 ID 应该返回 404")
    void getPlaylist_shouldReturn404ForNonExistent() throws Exception {
        mockMvc.perform(get("/api/playlists/99999"))
                .andExpect(status().isNotFound());
    }

    @Test
    @WithMockUser(username = "testuser")
    @DisplayName("POST /api/playlists 应该创建新歌单")
    void createPlaylist_shouldCreatePlaylist() throws Exception {
        PlaylistCreateDTO request = new PlaylistCreateDTO("New Playlist");

        mockMvc.perform(post("/api/playlists")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("New Playlist"))
                .andExpect(jsonPath("$.ownerUsername").value("testuser"));
    }

    @Test
    @DisplayName("POST /api/playlists 未认证应该返回 401")
    void createPlaylist_shouldReturn401WhenNotAuthenticated() throws Exception {
        PlaylistCreateDTO request = new PlaylistCreateDTO("New Playlist");

        mockMvc.perform(post("/api/playlists")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = "testuser")
    @DisplayName("DELETE /api/playlists/{id} 应该删除歌单")
    void deletePlaylist_shouldDeletePlaylist() throws Exception {
        Playlist playlist = playlistRepository.save(new Playlist("To Delete", testUser));

        mockMvc.perform(delete("/api/playlists/" + playlist.getId()))
                .andExpect(status().isNoContent());

        mockMvc.perform(get("/api/playlists/" + playlist.getId()))
                .andExpect(status().isNotFound());
    }
}
