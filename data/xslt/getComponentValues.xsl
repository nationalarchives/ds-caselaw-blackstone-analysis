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
        <xsl:text>eID|@|Para Num|@|xpath|@|text
</xsl:text>
        <xsl:apply-templates />
    </xsl:template>  
    
    <xsl:template match="//akn:p">   
        <xsl:if test="not(./ancestor::node()[name() = 'paragraph' or name() = 'level'])">
            <xsl:text>|@|</xsl:text><xsl:text>|@|</xsl:text><xsl:for-each select="./ancestor-or-self::node()"><xsl:value-of select="name(.)"/><xsl:if test="not(position() = last())">/</xsl:if></xsl:for-each><xsl:text>|@|</xsl:text><xsl:apply-templates mode="child" /><xsl:text>
</xsl:text>
        </xsl:if> 
    </xsl:template>  
    
    <xsl:template match="//akn:p|//akn:span[not(./ancestor::node()[name() = 'p'])]" mode="para">
        <xsl:param name="first_columns"/>
        <xsl:value-of select="$first_columns"/><xsl:text></xsl:text><xsl:for-each select="./ancestor-or-self::node()"><xsl:value-of select="name(.)"/><xsl:if test="not(position() = last())">/</xsl:if></xsl:for-each><xsl:text>|@|</xsl:text><xsl:apply-templates mode="child"/><xsl:text>
</xsl:text> 
    </xsl:template> 
    
    
    <xsl:template match="node()" mode="child">
        <xsl:value-of select="normalize-space(.)"/><xsl:text> </xsl:text>
    </xsl:template>
    

    <xsl:template match="//akn:level">       
        <xsl:apply-templates mode="para" >
            <xsl:with-param name="first_columns"><xsl:text></xsl:text><xsl:value-of select="./@eId"/><xsl:text>|@|</xsl:text><xsl:text>|@|</xsl:text></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="//akn:paragraph">        
        <xsl:apply-templates mode="para">
            <xsl:with-param name="first_columns"><xsl:text></xsl:text><xsl:value-of select="./@eId"/><xsl:text>|@|</xsl:text><xsl:value-of select="./akn:num"/><xsl:text>|@|</xsl:text></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="//akn:subparagraph">
        <xsl:apply-templates mode="para">
            <xsl:with-param name="first_columns"><xsl:text>|</xsl:text><xsl:value-of select="./akn:num"/><xsl:text>|@|</xsl:text></xsl:with-param>        
        </xsl:apply-templates>
    </xsl:template> 
    
    <xsl:template match="text()|@*" /> 
    
    <xsl:template match="text()|@*" mode="para" /> 
</xsl:stylesheet>