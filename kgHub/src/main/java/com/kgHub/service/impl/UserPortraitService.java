package com.kgHub.service.impl;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.kgHub.dao.UserPortraitMapper;
import com.kgHub.pojo.UserPortrait;
import com.kgHub.service.IUserPortraitService;

@Service
public class UserPortraitService implements IUserPortraitService {
	
	@Resource
	private UserPortraitMapper userPortraitMapper;

	@Override
	public int updateUserPortraitSelective(UserPortrait record) {
		return this.userPortraitMapper.updateByPrimaryKeySelective(record);
	}

	@Override
	public int insertSelective(UserPortrait record) {
		return this.userPortraitMapper.insertSelective(record);
	}

	@Override
	public UserPortrait selectByUserID(Integer userID) {
		return this.userPortraitMapper.selectByUserID(userID);
	}

}
