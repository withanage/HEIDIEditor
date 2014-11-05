<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
        version="2.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei="http://www.tei-c.org/ns/1.0"
        xmlns:exist="http://exist.sourceforge.net/NS/exist"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"
                doctype-public="-//NLM//DTD Book DTD v3.0 20080202//EN"/>

    <xsl:template match="article">
        <book>
            <xsl:apply-templates select="front/journal-meta"/>
            <xsl:apply-templates select="front/notes"/>
            <body>
                <book-part>
                    <xsl:attribute name="book-part-type">chapter</xsl:attribute>
                    <xsl:if test="front/article-meta/article-id">
                        <xsl:attribute name="id">
                            <xsl:value-of select="front/article-meta/article-id"/>
                        </xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates select="front/article-meta"/>
                    <xsl:copy-of select="body"/>
                    <xsl:copy-of select="back"/>
                </book-part>
            </body>
        </book>

    </xsl:template>

    <xsl:template match="front">
        <book-meta>
            <xsl:apply-templates select="journal-meta"/>
            <xsl:apply-templates select="article-meta/isbn"/>
        </book-meta>
    </xsl:template>

    <xsl:template match="journal-meta/journal-id[@journal-id-type]">
        <book-id>
            <xsl:attribute name="pub-id-type">
                <xsl:value-of select="@journal-id-type"/>
            </xsl:attribute>
            <xsl:copy-of select="node()"/>
        </book-id>
    </xsl:template>
    <xsl:template match="journal-meta/journal-id[not(@journal-id-type)]">
        <book-id>
            <xsl:copy-of select="@*|node()"/>
        </book-id>
    </xsl:template>


    <xsl:template match="journal-meta/issn|article-meta/isbn">
        <isbn>
            <xsl:copy-of select="@*|node()"/>
        </isbn>
    </xsl:template>


    <xsl:template match="journal-meta/publisher">
        <publisher>
            <xsl:copy-of select="@*|node()"/>
        </publisher>
    </xsl:template>

    <xsl:template match="front/notes">
        <book-front>
            <xsl:apply-templates />
        </book-front>
    </xsl:template>

    <xsl:template match="article-meta">
        <book-part-meta>
            <xsl:apply-templates select="article-categories"/>
            <xsl:apply-templates select="title-group"/>
            <xsl:copy-of select="contrib-group"/>
            <xsl:copy-of select="aff"/>
            <xsl:copy-of select="author-notes"/>
            <xsl:copy-of select="pub-date"/>
            <xsl:copy-of select="volume"/>
            <xsl:copy-of select="volume-id"/>
            <xsl:copy-of select="issue"/>
            <xsl:copy-of select="fpage"/>
            <xsl:copy-of select="lpage"/>
            <xsl:copy-of select="elocation-id"/>
            <xsl:copy-of select="supplementary-material"/>
            <xsl:copy-of select="history"/>
            <xsl:copy-of select="permission"/>
            <xsl:copy-of select="alternate-form"/>
            <xsl:copy-of select="abstract"/>
            <xsl:copy-of select="trans-abstract"/>
            <xsl:copy-of select="kwd-group"/>
            <xsl:copy-of select="counts"/>
            <xsl:copy-of select="email"/>
            <xsl:copy-of select="ext-link"/>
            <xsl:copy-of select="uri"/>
            <xsl:copy-of select="custom-meta-group"/>
            <xsl:copy-of select="notes"/>
        </book-part-meta>
    </xsl:template>

    <xsl:template match="article-categories">
        <book-part-categories>
            <xsl:copy-of select="subj-group"/>
        </book-part-categories>
    </xsl:template>

    <xsl:template match="title-group">
        <title-group>
            <title>
                <xsl:value-of select="article-title"/>
            </title>
            <xsl:copy-of select="subtitle"/>
            <xsl:copy-of select="trans-title-group"/>
            <xsl:copy-of select="alt-title"/>
            <xsl:copy-of select="fn-group"/>
        </title-group>
    </xsl:template>


</xsl:stylesheet>