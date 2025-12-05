<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:html="http://www.w3.org/1999/xhtml" 
    xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"
    xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
    exclude-result-prefixes="xs uk akn html"
    version="1.0">
    <!-- <xsl:output method="xml" encoding="UTF-8" omit-xml-declaration="no" indent="yes"/> -->
    <xsl:output method="text" encoding="UTF-8" omit-xml-declaration="yes" indent="yes"/>
    <xsl:strip-space elements="*"/>
    
    
    <xsl:template match="/">
        <xsl:text>text|@|type|@|href|@|isNeutral|@|canonical|@|year|@|origin|@|eID|@|num|@|path|@|context
</xsl:text>        
        <xsl:apply-templates />
    </xsl:template>    
    
    <xsl:template match="akn:ref">
        <xsl:value-of select="normalize-space(.)"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@uk:type"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@href"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@uk:isNeutral"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@uk:canonical"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@uk:year"/><xsl:text>|@|</xsl:text><xsl:value-of select="./@uk:origin"/>
        <xsl:text>|@|</xsl:text><xsl:value-of select="(ancestor::*/@eId)[1]"/>
        <xsl:text>|@|</xsl:text><xsl:value-of select="(ancestor::*/akn:num)[1]"/>
        <xsl:text>|@|</xsl:text><xsl:for-each select="./ancestor-or-self::node()"><xsl:value-of select="name(.)"/><xsl:if test="not(position() = last())">/</xsl:if></xsl:for-each>
        <xsl:text>|@|</xsl:text><xsl:apply-templates select="ancestor::akn:p[1]" mode="child"/>
        <xsl:text>
</xsl:text>
    </xsl:template>
    
    <xsl:template match="akn:p" mode="child">
        <xsl:apply-templates mode="child"/>
    </xsl:template>
    
    <xsl:template match="node()" mode="child">
        <xsl:value-of select="normalize-space(.)"/><xsl:text> </xsl:text>
    </xsl:template>
    
    <xsl:template match="text()|@*" /> 
</xsl:stylesheet>