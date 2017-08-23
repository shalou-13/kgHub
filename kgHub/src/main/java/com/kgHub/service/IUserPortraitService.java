package com.kgHub.service;

import com.kgHub.pojo.UserPortrait;

public interface IUserPortraitService {

	public int updateUserPortraitSelective(UserPortrait record);
	
	public int insertSelective(UserPortrait record);
	
	public UserPortrait selectByUserID(Integer userID);
}
