package com.kgHub.dao;

import java.util.List;

import com.kgHub.pojo.DeadPerson;

public interface DeadPersonMapper {
    int deleteByPrimaryKey(String ID);

    int insert(DeadPerson record);

    int insertSelective(DeadPerson record);

    DeadPerson selectByPrimaryKey(String ID);

    int updateByPrimaryKeySelective(DeadPerson record);

    int updateByPrimaryKey(DeadPerson record);
    
    List<DeadPerson> selectAllDeadPersons();
}