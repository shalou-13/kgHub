package com.kgHub.controller;

import javax.annotation.Resource;

import org.apache.http.HttpRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.kgHub.service.impl.ChildrenMissionService;

@Controller
public class ChildrenMissionsController {
	
	private static org.apache.log4j.Logger logger=org.apache.log4j.Logger.getLogger(ChildrenMissionsController.class);
	
	@Resource
	private ChildrenMissionService childrenMissionService=null;
	
	@RequestMapping("/GetAllChildMissions")
	@ResponseBody
	public void getAllChildMissions(HttpRequest request){
		return;
	}
	
}
