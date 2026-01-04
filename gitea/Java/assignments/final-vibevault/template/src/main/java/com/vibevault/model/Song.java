package com.vibevault.model;

import jakarta.persistence.*;

/**
 * 歌曲实体类
 * 
 * 需要实现：
 * - 将此类映射为数据库表 "songs"
 * - id 作为自增主键
 * - 每首歌曲属于一个歌单（多对一关系）
 */
public class Song {

    private Long id;

    private String title;

    private String artist;

    private int durationInSeconds;

    private Playlist playlist;

    public Song() {
    }

    public Song(String title, String artist, int durationInSeconds) {
        this.title = title;
        this.artist = artist;
        this.durationInSeconds = durationInSeconds;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getArtist() {
        return artist;
    }

    public int getDurationInSeconds() {
        return durationInSeconds;
    }

    public Playlist getPlaylist() {
        return playlist;
    }

    public void setPlaylist(Playlist playlist) {
        this.playlist = playlist;
    }
}
