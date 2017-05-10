package com.kgHub.pojo;

import java.util.Date;

public class InstituteInfo {
    private String id;

    private String instName;

    private String instCode;

    private String regisAddr;

    private Double longitude;

    private Double latitude;

    private String province;

    private String city;

    private String areaCode;

    private String legalPersonName;

    private String legalPersonID;

    private String orgType;

    private Byte orgSubType;

    private String busiScop;

    private String orgPhotos;

    private String orgTel;

    private String orgEmail;

    private String licenseScanning;

    private String codeScanning;

    private String docScanning;

    private Date foundTime;

    private Byte state;

    private String phaseID;

    private String sourceID;

    private Date insertTime;

    private String orgIntro;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id == null ? null : id.trim();
    }

    public String getInstName() {
        return instName;
    }

    public void setInstName(String instName) {
        this.instName = instName == null ? null : instName.trim();
    }

    public String getInstCode() {
        return instCode;
    }

    public void setInstCode(String instCode) {
        this.instCode = instCode == null ? null : instCode.trim();
    }

    public String getRegisAddr() {
        return regisAddr;
    }

    public void setRegisAddr(String regisAddr) {
        this.regisAddr = regisAddr == null ? null : regisAddr.trim();
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public String getProvince() {
        return province;
    }

    public void setProvince(String province) {
        this.province = province == null ? null : province.trim();
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city == null ? null : city.trim();
    }

    public String getAreaCode() {
        return areaCode;
    }

    public void setAreaCode(String areaCode) {
        this.areaCode = areaCode == null ? null : areaCode.trim();
    }

    public String getLegalPersonName() {
        return legalPersonName;
    }

    public void setLegalPersonName(String legalPersonName) {
        this.legalPersonName = legalPersonName == null ? null : legalPersonName.trim();
    }

    public String getLegalPersonID() {
        return legalPersonID;
    }

    public void setLegalPersonID(String legalPersonID) {
        this.legalPersonID = legalPersonID == null ? null : legalPersonID.trim();
    }

    public String getOrgType() {
        return orgType;
    }

    public void setOrgType(String orgType) {
        this.orgType = orgType == null ? null : orgType.trim();
    }

    public Byte getOrgSubType() {
        return orgSubType;
    }

    public void setOrgSubType(Byte orgSubType) {
        this.orgSubType = orgSubType;
    }

    public String getBusiScop() {
        return busiScop;
    }

    public void setBusiScop(String busiScop) {
        this.busiScop = busiScop == null ? null : busiScop.trim();
    }

    public String getOrgPhotos() {
        return orgPhotos;
    }

    public void setOrgPhotos(String orgPhotos) {
        this.orgPhotos = orgPhotos == null ? null : orgPhotos.trim();
    }

    public String getOrgTel() {
        return orgTel;
    }

    public void setOrgTel(String orgTel) {
        this.orgTel = orgTel == null ? null : orgTel.trim();
    }

    public String getOrgEmail() {
        return orgEmail;
    }

    public void setOrgEmail(String orgEmail) {
        this.orgEmail = orgEmail == null ? null : orgEmail.trim();
    }

    public String getLicenseScanning() {
        return licenseScanning;
    }

    public void setLicenseScanning(String licenseScanning) {
        this.licenseScanning = licenseScanning == null ? null : licenseScanning.trim();
    }

    public String getCodeScanning() {
        return codeScanning;
    }

    public void setCodeScanning(String codeScanning) {
        this.codeScanning = codeScanning == null ? null : codeScanning.trim();
    }

    public String getDocScanning() {
        return docScanning;
    }

    public void setDocScanning(String docScanning) {
        this.docScanning = docScanning == null ? null : docScanning.trim();
    }

    public Date getFoundTime() {
        return foundTime;
    }

    public void setFoundTime(Date foundTime) {
        this.foundTime = foundTime;
    }

    public Byte getState() {
        return state;
    }

    public void setState(Byte state) {
        this.state = state;
    }

    public String getPhaseID() {
        return phaseID;
    }

    public void setPhaseID(String phaseID) {
        this.phaseID = phaseID == null ? null : phaseID.trim();
    }

    public String getSourceID() {
        return sourceID;
    }

    public void setSourceID(String sourceID) {
        this.sourceID = sourceID == null ? null : sourceID.trim();
    }

    public Date getInsertTime() {
        return insertTime;
    }

    public void setInsertTime(Date insertTime) {
        this.insertTime = insertTime;
    }

    public String getOrgIntro() {
        return orgIntro;
    }

    public void setOrgIntro(String orgIntro) {
        this.orgIntro = orgIntro == null ? null : orgIntro.trim();
    }
}