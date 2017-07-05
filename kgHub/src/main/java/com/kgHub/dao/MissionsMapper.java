package com.kgHub.dao;

import java.util.List;

import com.kgHub.pojo.Missions;
import com.kgHub.pojo.MissionsWithBLOBs;

public interface MissionsMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(MissionsWithBLOBs record);

    int insertSelective(MissionsWithBLOBs record);

    MissionsWithBLOBs selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(MissionsWithBLOBs record);

    int updateByPrimaryKeyWithBLOBs(MissionsWithBLOBs record);

    int updateByPrimaryKey(Missions record);
    
    List<MissionsWithBLOBs> selectAllMissions();
}