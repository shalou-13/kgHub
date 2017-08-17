package com.kgHub.dao;

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
}