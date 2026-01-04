package com.vibevault.core;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vibevault.dto.PlaylistCreateDTO;
import com.vibevault.dto.SongCreateDTO;
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
 * Core 轨道测试：基础安全骨架
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class CoreSecurityTest {

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
    @DisplayName("GET /api/playlists 应该允许匿名访问")
    void getPlaylists_shouldAllowAnonymous() throws Exception {
        mockMvc.perform(get("/api/playlists"))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("GET /api/playlists/{id} 应该允许匿名访问")
    void getPlaylistById_shouldAllowAnonymous() throws Exception {
        Playlist playlist = playlistRepository.save(new Playlist("Test", testUser));
        
        mockMvc.perform(get("/api/playlists/" + playlist.getId()))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("POST /api/playlists 未认证应该返回 401")
    void createPlaylist_shouldRequireAuth() throws Exception {
        PlaylistCreateDTO request = new PlaylistCreateDTO("New Playlist");

        mockMvc.perform(post("/api/playlists")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("DELETE /api/playlists/{id} 未认证应该返回 401")
    void deletePlaylist_shouldRequireAuth() throws Exception {
        Playlist playlist = playlistRepository.save(new Playlist("Test", testUser));

        mockMvc.perform(delete("/api/playlists/" + playlist.getId()))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("POST /api/playlists/{id}/songs 未认证应该返回 401")
    void addSong_shouldRequireAuth() throws Exception {
        Playlist playlist = playlistRepository.save(new Playlist("Test", testUser));
        SongCreateDTO song = new SongCreateDTO("Song", "Artist", 180);

        mockMvc.perform(post("/api/playlists/" + playlist.getId() + "/songs")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(song)))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = "testuser")
    @DisplayName("POST /api/playlists 认证后应该允许访问")
    void createPlaylist_shouldAllowAuthenticated() throws Exception {
        PlaylistCreateDTO request = new PlaylistCreateDTO("New Playlist");

        mockMvc.perform(post("/api/playlists")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated());
    }
}
