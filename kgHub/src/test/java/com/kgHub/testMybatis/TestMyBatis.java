package com.kgHub.testMybatis;

import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.alibaba.fastjson.JSON;
import com.kgHub.pojo.InstituteInfo;
import com.kgHub.service.IInstituteInfoService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath*:spring-mybatis.xml" })

public class TestMyBatis {
	
	private static Logger logger = Logger.getLogger(TestMyBatis.class);
	
	@Resource
	private IInstituteInfoService instituteInfoService = null;
	
	
	@Test
	public void Test(){
		InstituteInfo institute = instituteInfoService.getInstituteInfoById("08B97425E9AE40E2B9B313D1DD35BA16");
		logger.info(JSON.toJSONString(institute));
	}
	

}
