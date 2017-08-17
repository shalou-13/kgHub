package com.kgHub.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.kgHub.methods.HanlpHandler;
import com.kgHub.methods.XMLExtendReader;
import com.kgHub.pojo.ChildrenMissionsWithBLOBs;
import com.kgHub.pojo.GraphNode;
import com.kgHub.pojo.GraphSearchServerConfig;
import com.kgHub.pojo.MissionsWithBLOBs;
import com.kgHub.service.impl.ChildrenMissionService;
import com.kgHub.service.impl.MissionService;
import com.kgHub.util.HttpClientHandler;
import com.kgHub.util.JsonHandler;

@Controller
public class TaskController {

	private static Logger logger = Logger.getLogger(TaskController.class);
	
	@Resource
	private  MissionService missionService;
	@Resource
	private ChildrenMissionService childrenMissionService;
	
	@RequestMapping(value="/searchGraph",method=RequestMethod.POST)
	@ResponseBody
	public void searchGraph(
			HttpServletRequest request, HttpServletResponse response) {
		try {
			String jsonStr = JsonHandler.readJsonFromRequest(request);
			JSONObject obj = JSONObject.parseObject(jsonStr);
			String text = obj.getString("text");
			Map<String,Map<String,String>> keywordList = HanlpHandler.nlpspecific(text);
			MissionsWithBLOBs missionsWithBLOBs = new MissionsWithBLOBs();
			missionsWithBLOBs.setRkeyword(text);
			missionsWithBLOBs.setNkeyword(JSON.toJSONString(keywordList.get("n")));
			missionsWithBLOBs.setVkeyword(JSON.toJSONString(keywordList.get("v")));
			missionsWithBLOBs.setAkeyword(JSON.toJSONString(keywordList.get("ad")));
			missionsWithBLOBs.setState(1);
			missionsWithBLOBs.setUserID(2);
			boolean missionID = missionService.insertMission(missionsWithBLOBs);
			if(missionID){
				XMLExtendReader reader = new XMLExtendReader();
				ArrayList<GraphNode> graphList = reader.getGraphList();
				HashMap<String, Object> result = new HashMap<String, Object>();
				for(GraphNode graph: graphList){
					if(graph.searchServers.size()!=0){
						GraphSearchServerConfig server = graph.searchServers.get(0);
						ChildrenMissionsWithBLOBs childrenMission=new ChildrenMissionsWithBLOBs();
						childrenMission.setState(1);
						childrenMission.setPId(missionsWithBLOBs.getId());
						childrenMission.setGraphID(graph.getId());
						boolean subMissionID = childrenMissionService.insertChildMission(childrenMission);
						if(subMissionID){
							Map<String, Object> json = new HashMap<String, Object>();
							json.put("graphID", graph.getId());
							json.put("typeID", graph.getTypeID());
							json.put("engine", graph.getSearchServers().get(0).getEngineClass());
							json.put("subMissionID", childrenMission.getId());
							String sub_result = HttpClientHandler.doPost(server.getEnterPath(), server.getHost(), server.getScheme(), JSON.toJSONString(json));
							childrenMissionService.changeState(childrenMission.getId(), 3);
							missionService.changeStateById(missionsWithBLOBs.getId(), 3);
							result.put(graph.getId(), JSON.parse(sub_result));
						}else{
							JsonHandler.writeJsonStreamFromResponse(response, JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3004, ""))).toString());
						}
					}else{
						JsonHandler.writeJsonStreamFromResponse(response, JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3005, ""))).toString());
					}
				}
				JsonHandler.writeJsonStreamFromResponse(response, JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3000, result))).toString());
				
			}else{
				JsonHandler.writeJsonStreamFromResponse(response, JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3003, ""))).toString());
			}
			
		} catch (Exception e) {
			e.printStackTrace();
			logger.error(e.toString());;
			JsonHandler.writeJsonStreamFromResponse(response, JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3001, ""))).toString());
		}
	}
}
