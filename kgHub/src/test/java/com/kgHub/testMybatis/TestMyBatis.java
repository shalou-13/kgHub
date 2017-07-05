package com.kgHub.testMybatis;

import java.util.ArrayList;

import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.alibaba.fastjson.JSON;
import com.kgHub.dao.ChildrenMissionsMapper;
import com.kgHub.pojo.ChildrenMissions;
import com.kgHub.pojo.InstituteInfo;
import com.kgHub.pojo.Missions;
import com.kgHub.pojo.MissionsWithBLOBs;
import com.kgHub.service.IChildrenMissionService;
import com.kgHub.service.IInstituteInfoService;
import com.kgHub.service.IMissionService;
import com.kgHub.service.impl.ChildrenMissionService;
import com.kgHub.service.impl.MissionService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath*:spring-mybatis.xml" })

public class TestMyBatis {
	
	private static Logger logger = Logger.getLogger(TestMyBatis.class);
	
	@Resource
	private IInstituteInfoService instituteInfoService=null;
	
	@Resource
	private IChildrenMissionService childrenMissionService=null;
	//private ChildrenMissionsMapper mapper;
	
	@Resource
	private IMissionService missionService=null;

	/*@Test
	public void Test(){
		InstituteInfo institute=instituteInfoService.getInstituteInfoById("08B97425E9AE40E2B9B313D1DD35BA16");
		logger.info(JSON.toJSONString(institute));
	}*/
	
	/*@Test
	public void Test1(){
		ArrayList<InstituteInfo> infos=instituteInfoService.getAllInstituteInfos();
		System.out.println(JSON.toJSONString(infos));
	}*/
	
	/*@Test
	public void Test2(){
		System.out.println(childrenMissionService.changeState(6,1));
	}*/
	
	/*@Test
	public void Test3(){
		ArrayList<ChildrenMissions> missions=childrenMissionService.GetAllChildMissions();
		for(ChildrenMissions iter:missions){
			iter.show();
		}
	}*/
	
	/*@Test
	public void Test4(){
		ChildrenMissions child=mapper.selectByPrimaryKey(3);
		logger.info(JSON.toJSONString(child));
	}*/
	
	/*@Test
	public void Test5(){
		System.out.println(childrenMissionService.insertChildMission(3,0));
	}*/
	
	@Test
	public void Test6(){
		ArrayList<MissionsWithBLOBs> missions=missionService.getAllMissions();
		for(MissionsWithBLOBs iter:missions){
			iter.show();
		}
	}
	
	/*@Test
	public void Test7(){
		System.out.println(missionService.insertMission("12345","","","",0));
	}*/
	
	@Test
	public void Test8(){
		System.out.println(missionService.changeStateById(1,1));
	}
}
