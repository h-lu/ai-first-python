package com.vibevault.core;

import com.vibevault.model.Playlist;
import com.vibevault.model.Song;
import com.vibevault.model.User;
import com.vibevault.repository.PlaylistRepository;
import com.vibevault.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Core 轨道测试：实体与持久化
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class CoreEntityTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Test
    @DisplayName("User 实体应该能够正确保存和读取")
    void user_shouldBePersisted() {
        User user = new User("testuser", passwordEncoder.encode("password123"));
        User saved = userRepository.save(user);

        assertNotNull(saved.getId(), "User ID should be generated");
        assertEquals("testuser", saved.getUsername());
    }

    @Test
    @DisplayName("Playlist 实体应该能够正确保存和读取")
    void playlist_shouldBePersisted() {
        User user = userRepository.save(new User("owner", passwordEncoder.encode("pass")));
        Playlist playlist = new Playlist("My Playlist", user);
        Playlist saved = playlistRepository.save(playlist);

        assertNotNull(saved.getId(), "Playlist ID should be generated");
        assertEquals("My Playlist", saved.getName());
        assertEquals("owner", saved.getOwner().getUsername());
    }

    @Test
    @DisplayName("Playlist 与 Song 的一对多关系应该正确工作")
    void playlist_shouldHaveSongs() {
        User user = userRepository.save(new User("owner", passwordEncoder.encode("pass")));
        Playlist playlist = new Playlist("My Playlist", user);
        Song song1 = new Song("Song 1", "Artist 1", 180);
        Song song2 = new Song("Song 2", "Artist 2", 200);

        playlist.addSong(song1);
        playlist.addSong(song2);
        Playlist saved = playlistRepository.save(playlist);

        assertEquals(2, saved.getSongs().size());
    }

    @Test
    @DisplayName("User 的 username 应该是唯一的")
    void user_usernameShouldBeUnique() {
        userRepository.save(new User("uniqueuser", passwordEncoder.encode("pass1")));

        assertThrows(Exception.class, () -> {
            userRepository.saveAndFlush(new User("uniqueuser", passwordEncoder.encode("pass2")));
        }, "Should throw exception for duplicate username");
    }

    @Test
    @DisplayName("Playlist 删除时应该级联删除 Song")
    void playlist_deleteShouldCascadeToSongs() {
        User user = userRepository.save(new User("owner", passwordEncoder.encode("pass")));
        Playlist playlist = new Playlist("My Playlist", user);
        playlist.addSong(new Song("Song 1", "Artist", 180));
        Playlist saved = playlistRepository.save(playlist);
        Long playlistId = saved.getId();

        playlistRepository.delete(saved);
        playlistRepository.flush();

        assertFalse(playlistRepository.findById(playlistId).isPresent());
    }
}
