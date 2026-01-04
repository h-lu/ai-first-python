package com.vibevault.challenge;

import com.fasterxml.jackson.databind.ObjectMapper;
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
 * Challenge 轨道测试：所有权检查
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class ChallengeOwnershipTest {

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

    private User owner;
    private User otherUser;
    private Playlist ownerPlaylist;

    @BeforeEach
    void setUp() {
        owner = userRepository.save(new User("owner", passwordEncoder.encode("password")));
        otherUser = userRepository.save(new User("other", passwordEncoder.encode("password")));
        ownerPlaylist = playlistRepository.save(new Playlist("Owner's Playlist", owner));
    }

    @Test
    @WithMockUser(username = "owner")
    @DisplayName("所有者应该能删除自己的歌单")
    void owner_shouldBeAbleToDeleteOwnPlaylist() throws Exception {
        mockMvc.perform(delete("/api/playlists/" + ownerPlaylist.getId()))
                .andExpect(status().isNoContent());
    }

    @Test
    @WithMockUser(username = "other")
    @DisplayName("非所有者不应该能删除他人的歌单")
    void nonOwner_shouldNotBeAbleToDeleteOthersPlaylist() throws Exception {
        mockMvc.perform(delete("/api/playlists/" + ownerPlaylist.getId()))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(username = "owner")
    @DisplayName("所有者应该能向自己的歌单添加歌曲")
    void owner_shouldBeAbleToAddSong() throws Exception {
        SongCreateDTO song = new SongCreateDTO("New Song", "Artist", 180);

        mockMvc.perform(post("/api/playlists/" + ownerPlaylist.getId() + "/songs")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(song)))
                .andExpect(status().isCreated());
    }

    @Test
    @WithMockUser(username = "other")
    @DisplayName("非所有者不应该能向他人的歌单添加歌曲")
    void nonOwner_shouldNotBeAbleToAddSong() throws Exception {
        SongCreateDTO song = new SongCreateDTO("New Song", "Artist", 180);

        mockMvc.perform(post("/api/playlists/" + ownerPlaylist.getId() + "/songs")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(song)))
                .andExpect(status().isForbidden());
    }
}
