package com.kgHub.dao;

import java.util.List;

import com.kgHub.pojo.InstituteInfo;

public interface InstituteInfoMapper {
    int deleteByPrimaryKey(String id);

    int insert(InstituteInfo record);

    int insertSelective(InstituteInfo record);

    InstituteInfo selectByPrimaryKey(String id);

    int updateByPrimaryKeySelective(InstituteInfo record);

    int updateByPrimaryKeyWithBLOBs(InstituteInfo record);

    int updateByPrimaryKey(InstituteInfo record);
    
    List<InstituteInfo> selectAllInstituteInfos();
}