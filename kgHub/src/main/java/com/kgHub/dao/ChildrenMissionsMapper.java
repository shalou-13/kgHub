package com.kgHub.dao;

import java.util.ArrayList;

import org.apache.ibatis.annotations.Param;

import com.kgHub.pojo.ChildrenMissions;
import com.kgHub.pojo.ChildrenMissionsWithBLOBs;

public interface ChildrenMissionsMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(ChildrenMissionsWithBLOBs record);

    int insertSelective(ChildrenMissionsWithBLOBs record);

    ChildrenMissionsWithBLOBs selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(ChildrenMissionsWithBLOBs record);

    int updateByPrimaryKeyWithBLOBs(ChildrenMissionsWithBLOBs record);

    int updateByPrimaryKey(ChildrenMissions record);
    
    ArrayList<ChildrenMissionsWithBLOBs> selectChildMissionsByUserID(@Param("userID")Integer userID, @Param("graphID")String graphID);
    
}