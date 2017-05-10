package com.kgHub.pojo;

import java.util.Date;

public class DeadPerson {
    private String ID;

    private String recordID;

    private String name;

    private String IDCardCode;

    private Integer age;

    private Integer disease;

    private String instCode;

    private String areaCode;

    private Date deadDate;

    private Date birthDay;

    private String phaseID;

    private Date insertTime;

    private Integer gender;

    public String getID() {
        return ID;
    }

    public void setID(String ID) {
        this.ID = ID == null ? null : ID.trim();
    }

    public String getRecordID() {
        return recordID;
    }

    public void setRecordID(String recordID) {
        this.recordID = recordID == null ? null : recordID.trim();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name == null ? null : name.trim();
    }

    public String getIDCardCode() {
        return IDCardCode;
    }

    public void setIDCardCode(String IDCardCode) {
        this.IDCardCode = IDCardCode == null ? null : IDCardCode.trim();
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getDisease() {
        return disease;
    }

    public void setDisease(Integer disease) {
        this.disease = disease;
    }

    public String getInstCode() {
        return instCode;
    }

    public void setInstCode(String instCode) {
        this.instCode = instCode == null ? null : instCode.trim();
    }

    public String getAreaCode() {
        return areaCode;
    }

    public void setAreaCode(String areaCode) {
        this.areaCode = areaCode == null ? null : areaCode.trim();
    }

    public Date getDeadDate() {
        return deadDate;
    }

    public void setDeadDate(Date deadDate) {
        this.deadDate = deadDate;
    }

    public Date getBirthDay() {
        return birthDay;
    }

    public void setBirthDay(Date birthDay) {
        this.birthDay = birthDay;
    }

    public String getPhaseID() {
        return phaseID;
    }

    public void setPhaseID(String phaseID) {
        this.phaseID = phaseID == null ? null : phaseID.trim();
    }

    public Date getInsertTime() {
        return insertTime;
    }

    public void setInsertTime(Date insertTime) {
        this.insertTime = insertTime;
    }

    public Integer getGender() {
        return gender;
    }

    public void setGender(Integer gender) {
        this.gender = gender;
    }
}