package com.vibevault.advanced;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.model.Playlist;
import com.vibevault.model.User;
import com.vibevault.repository.PlaylistRepository;
import com.vibevault.repository.UserRepository;
import com.vibevault.service.PlaylistService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Advanced 轨道测试：高级查询
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class AdvancedQueryTest {

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private PlaylistService playlistService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private User user1;
    private User user2;

    @BeforeEach
    void setUp() {
        user1 = userRepository.save(new User("user1", passwordEncoder.encode("password")));
        user2 = userRepository.save(new User("user2", passwordEncoder.encode("password")));

        playlistRepository.save(new Playlist("Rock Classics", user1));
        playlistRepository.save(new Playlist("Jazz Favorites", user1));
        playlistRepository.save(new Playlist("Pop Hits", user2));
    }

    @Test
    @DisplayName("应该能够按所有者查询歌单")
    void findByOwner_shouldReturnOwnerPlaylists() {
        List<Playlist> result = playlistRepository.findByOwner(user1);
        assertEquals(2, result.size());
    }

    @Test
    @DisplayName("应该能够按名称模糊搜索歌单")
    void findByNameContaining_shouldReturnMatchingPlaylists() {
        List<Playlist> result = playlistRepository.findByNameContainingIgnoreCase("favorites");
        assertEquals(1, result.size());
        assertEquals("Jazz Favorites", result.get(0).getName());
    }

    @Test
    @DisplayName("searchPlaylists 服务方法应该正常工作")
    void searchPlaylists_shouldWork() {
        List<PlaylistDTO> result = playlistService.searchPlaylists("Rock");
        assertEquals(1, result.size());
        assertEquals("Rock Classics", result.get(0).name());
    }

    @Test
    @DisplayName("copyPlaylist 应该复制歌单")
    void copyPlaylist_shouldCopyPlaylist() {
        Playlist original = playlistRepository.findByNameContainingIgnoreCase("Rock").get(0);
        
        PlaylistDTO copy = playlistService.copyPlaylist(original.getId(), "Rock Classics Copy", "user1");
        
        assertNotNull(copy);
        assertEquals("Rock Classics Copy", copy.name());
        assertNotEquals(original.getId(), copy.id());
    }
}
