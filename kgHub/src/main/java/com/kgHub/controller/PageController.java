package com.kgHub.controller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class PageController {
	
	
	@RequestMapping("/test")
	public ModelAndView test(HttpServletRequest request,
			HttpServletResponse response) {
		ModelAndView mav = new ModelAndView("test");
		return mav;
	}
	@RequestMapping("/kgHubSearch")
	public ModelAndView kgHubSearch(HttpServletRequest request,
			HttpServletResponse response) {
		ModelAndView mav = new ModelAndView("kgHubSearch");
		return mav;
	}

}
