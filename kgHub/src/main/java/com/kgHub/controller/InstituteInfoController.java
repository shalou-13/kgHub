package com.kgHub.controller;

import java.util.Map;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.alibaba.fastjson.JSONObject;
import com.kgHub.pojo.InstituteInfo;
import com.kgHub.service.impl.InstituteInfoService;
import com.kgHub.util.JsonHandler;

@Controller
public class InstituteInfoController {
	
	private static Logger logger = Logger.getLogger(InstituteInfoController.class);
	
	@Resource
	private  InstituteInfoService instituteInfoService = null;
	
	@RequestMapping(value="/getInstituteInfoByID",method=RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> getInstituteInfoByID(
			HttpServletRequest request, HttpServletResponse response) {
		try {
			String jsonStr = JsonHandler.readJsonFromRequest(request);
			JSONObject obj = JSONObject.parseObject(jsonStr);
			String id = obj.getString("id");
			
			InstituteInfo instituteInfo = instituteInfoService.getInstituteInfoById(id);
			if(instituteInfo==null)
				return JsonHandler.writeJsontoResponse(3002, "");
			
			return JsonHandler.writeJsontoResponse(3000, instituteInfo);
		} catch (Exception e) {
			e.printStackTrace();
			logger.error(e.toString());;
			return JsonHandler.writeJsontoResponse(3001, "");
		}
	}

}
