package com.vibevault.model;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * 歌单实体类
 * 
 * 需要实现：
 * - 将此类映射为数据库表 "playlists"
 * - id 作为自增主键
 * - name 不能为空
 * - 每个歌单属于一个用户（多对一关系）
 * - 一个歌单包含多首歌曲（一对多关系）
 * - 删除歌单时应级联删除其中的歌曲
 */
public class Playlist {

    private Long id;

    private String name;

    private User owner;

    private List<Song> songs = new ArrayList<>();

    protected Playlist() {
    }

    public Playlist(String name, User owner) {
        this.name = name;
        this.owner = owner;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public User getOwner() {
        return owner;
    }

    public List<Song> getSongs() {
        return Collections.unmodifiableList(songs);
    }

    /**
     * 向歌单添加歌曲
     * 提示：需要维护双向关系
     */
    public void addSong(Song song) {
        // TODO: 实现添加歌曲逻辑
    }

    /**
     * 从歌单移除歌曲
     * 提示：需要维护双向关系
     */
    public void removeSong(Song song) {
        // TODO: 实现移除歌曲逻辑
    }
}
