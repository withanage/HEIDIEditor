<?xml version="1.0"?>
<xsl:stylesheet
        version="2.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei="http://www.tei-c.org/ns/1.0"
        xmlns:exist="http://exist.sourceforge.net/NS/exist"
        xpath-default-namespace="http://www.tei-c.org/ns/1.0"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        exclude-result-prefixes="#all">

    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="article">

        <book>
            <xsl:apply-templates select="front/journal-meta"/>
            <xsl:apply-templates select="front/note"/>
            <body>
                <book-part>
                    <xsl:attribute name="book-part-type">chapter</xsl:attribute>
                    <xsl:apply-templates select="front/article-meta"/>
                    <xsl:apply-templates select="body"/>
                    <xsl:apply-templates select="back"/>
                </book-part>
            </body>
        </book>

    </xsl:template>

    <xsl:template match="front/journal-meta">
        <book-meta>
            <xsl:apply-templates />
        </book-meta>
    </xsl:template>

    <xsl:template match="journal-meta/journal-id">
        <book-id>
            <xsl:copy-of select="@*|node()"/>
        </book-id>
    </xsl:template>

    <!-- there is no issn tag in book-meta
        convert <issn> to @book-id-type='issn' -->
    <xsl:template match="journal-meta/issn">
        <book-id>
            <xsl:attribute name="book-id-type">
                <xsl:value-of select="name()"/>
            </xsl:attribute>
            <xsl:copy-of select="node()"/>
        </book-id>
    </xsl:template>

    <xsl:template match="journal-meta/publisher">
        <publisher>
            <xsl:copy-of select="@*|node()"/>
        </publisher>
    </xsl:template>

    <xsl:template match="notes">
        <notes>
            <xsl:copy-of select="@*|node()"/>
        </notes>
    </xsl:template>

    <xsl:template match="front/article-meta">
        <book-part-meta>
            <xsl:apply-templates />
        </book-part-meta>
    </xsl:template>

    <xsl:template match="body">
        <body>
            <xsl:copy-of select="@*|node()"/>
        </body>
    </xsl:template>

    <xsl:template match="back">
        <back>
            <xsl:copy-of select="@*|node()"/>
        </back>
    </xsl:template>

</xsl:stylesheet>