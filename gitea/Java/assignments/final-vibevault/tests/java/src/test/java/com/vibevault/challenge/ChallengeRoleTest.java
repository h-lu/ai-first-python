package com.vibevault.challenge;

import com.fasterxml.jackson.databind.ObjectMapper;
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
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Challenge 轨道测试：角色权限
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class ChallengeRoleTest {

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

    private User regularUser;
    private User adminUser;
    private Playlist userPlaylist;

    @BeforeEach
    void setUp() {
        regularUser = new User("regularuser", passwordEncoder.encode("password"), "ROLE_USER");
        userRepository.save(regularUser);
        
        adminUser = new User("admin", passwordEncoder.encode("password"), "ROLE_ADMIN");
        userRepository.save(adminUser);
        
        userPlaylist = playlistRepository.save(new Playlist("User's Playlist", regularUser));
    }

    @Test
    @WithMockUser(username = "admin", roles = {"ADMIN"})
    @DisplayName("管理员应该能删除任何用户的歌单")
    void admin_shouldBeAbleToDeleteAnyPlaylist() throws Exception {
        mockMvc.perform(delete("/api/playlists/" + userPlaylist.getId()))
                .andExpect(status().isNoContent());
    }

    @Test
    @WithMockUser(username = "regularuser", roles = {"USER"})
    @DisplayName("普通用户应该能删除自己的歌单")
    void user_shouldBeAbleToDeleteOwnPlaylist() throws Exception {
        mockMvc.perform(delete("/api/playlists/" + userPlaylist.getId()))
                .andExpect(status().isNoContent());
    }

    @Test
    @WithMockUser(username = "anotheruser", roles = {"USER"})
    @DisplayName("普通用户不应该能删除他人的歌单")
    void user_shouldNotBeAbleToDeleteOthersPlaylist() throws Exception {
        mockMvc.perform(delete("/api/playlists/" + userPlaylist.getId()))
                .andExpect(status().isForbidden());
    }
}
