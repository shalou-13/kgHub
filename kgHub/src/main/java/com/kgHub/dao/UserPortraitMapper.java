package com.kgHub.dao;

import com.kgHub.pojo.UserPortrait;

public interface UserPortraitMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(UserPortrait record);

    int insertSelective(UserPortrait record);

    UserPortrait selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(UserPortrait record);

    int updateByPrimaryKeyWithBLOBs(UserPortrait record);

    int updateByPrimaryKey(UserPortrait record);
    
    UserPortrait selectByUserID(Integer userID);
}