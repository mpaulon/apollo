import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_nfo(nfo_file: Path):
    pass

def create_nfo(
    title: str,
    original_title: str,
    plot: str,
    tmdbid: str,
    year: str,
    output: Path,
):
    root = ET.Element("movie")
    ET.SubElement(root, "title").text = title
    ET.SubElement(root, "originaltitle").text = original_title
    ET.SubElement(root, "plot").text = plot
    ET.SubElement(root, "year").text = year
    ET.SubElement(root, "tmdbid").text = tmdbid
    ET.SubElement(root, "lockdata").text = "true"
    tree = ET.ElementTree(root)
    ET.indent(tree)
    ET.dump(tree)
    tree.write(
        output, encoding="utf-8", xml_declaration=True, short_empty_elements=False
    )


if __name__ == "__main__":
    create_nfo("Tenet", "Tenet", "", "", "", Path("test.nfo"))

"""
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
  <plot>Armed with only one word - Tenet - and fighting for the survival of the entire world, the Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.</plot>
  <lockdata>false</lockdata>
  <dateadded>2024-05-16 18:30:08</dateadded>
  <title>Tenet</title>
  <originaltitle>Tenet</originaltitle>
  <director>Christopher Nolan</director>
  <writer>Christopher Nolan</writer>
  <credits>Christopher Nolan</credits>
  <trailer>plugin://plugin.video.youtube/?action=play_video&amp;videoid=KJP5RunZUKk</trailer>
  <trailer>plugin://plugin.video.youtube/?action=play_video&amp;videoid=AZGcmvrTX9M</trailer>
  <trailer>plugin://plugin.video.youtube/?action=play_video&amp;videoid=L3pk_TBkihU</trailer>
  <trailer>plugin://plugin.video.youtube/?action=play_video&amp;videoid=LdOM0x0XDMo</trailer>
  <rating>7.183</rating>
  <year>2020</year>
  <mpaa>PG-13</mpaa>
  <imdbid>tt6723592</imdbid>
  <tmdbid>577922</tmdbid>
  <premiered>2020-08-22</premiered>
  <releasedate>2020-08-22</releasedate>
  <criticrating>69</criticrating>
  <runtime>150</runtime>
  <tagline>Time runs out.</tagline>
  <country>United Kingdom</country>
  <country>United States of America</country>
  <genre>Action</genre>
  <genre>Thriller</genre>
  <genre>Science Fiction</genre>
  <studio>Warner Bros. Pictures</studio>
  <studio>Syncopy</studio>
  <tag>assassin</tag>
  <tag>espionage</tag>
  <tag>spy</tag>
  <tag>time travel</tag>
  <tag>mumbai (bombay), india</tag>
  <tag>arms dealer</tag>
  <tag>terrorism</tag>
  <tag>terrorist attack</tag>
  <tag>nuclear weapons</tag>
  <tag>terrorist plot</tag>
  <tag>backwards</tag>
  <tag>alternate timeline</tag>
  <tag>oslo, norway</tag>
  <tag>time paradox</tag>
  <tag>kyiv (kiev), ukraine</tag>
  <tag>complex</tag>
  <tag>intense</tag>
  <tag>ambiguous</tag>
  <tag>dubious</tag>
  <art>
    <poster>/cocotte/media/films/Tenet-poster.jpg</poster>
    <fanart>/cocotte/media/films/Tenet-backdrop.jpg</fanart>
  </art>
  <actor>
    <name>John David Washington</name>
    <role>The Protagonist</role>
    <type>Actor</type>
    <sortorder>0</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/J/John David Washington/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Robert Pattinson</name>
    <role>Neil</role>
    <type>Actor</type>
    <sortorder>1</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/R/Robert Pattinson/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Elizabeth Debicki</name>
    <role>Kat</role>
    <type>Actor</type>
    <sortorder>2</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/E/Elizabeth Debicki/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Kenneth Branagh</name>
    <role>Andrei Sator</role>
    <type>Actor</type>
    <sortorder>3</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/K/Kenneth Branagh/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Dimple Kapadia</name>
    <role>Priya</role>
    <type>Actor</type>
    <sortorder>4</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/D/Dimple Kapadia/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Himesh Patel</name>
    <role>Mahir</role>
    <type>Actor</type>
    <sortorder>5</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/H/Himesh Patel/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Aaron Taylor-Johnson</name>
    <role>Ives</role>
    <type>Actor</type>
    <sortorder>6</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/A/Aaron Taylor-Johnson/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Michael Caine</name>
    <role>Sir Michael Crosby</role>
    <type>Actor</type>
    <sortorder>7</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/M/Michael Caine/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Clémence Poésy</name>
    <role>Barbara</role>
    <type>Actor</type>
    <sortorder>8</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/C/Clémence Poésy/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Martin Donovan</name>
    <role>Fay</role>
    <type>Actor</type>
    <sortorder>9</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/M/Martin Donovan/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Yuri Kolokolnikov</name>
    <role>Volkov</role>
    <type>Actor</type>
    <sortorder>10</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/Y/Yuri Kolokolnikov/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Anthony Molinari</name>
    <role>Rohan</role>
    <type>Actor</type>
    <sortorder>11</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/A/Anthony Molinari/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Laurie Shepherd</name>
    <role>Max</role>
    <type>Actor</type>
    <sortorder>12</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/L/Laurie Shepherd/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Fiona Dourif</name>
    <role>Wheeler</role>
    <type>Actor</type>
    <sortorder>13</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/F/Fiona Dourif/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Juhan Ulfsak</name>
    <role>Passenger</role>
    <type>Actor</type>
    <sortorder>14</sortorder>
    <thumb>/var/lib/jellyfin/metadata/People/J/Juhan Ulfsak/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Christopher Nolan</name>
    <role>Producer</role>
    <type>Producer</type>
    <thumb>/var/lib/jellyfin/metadata/People/C/Christopher Nolan/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Emma Thomas</name>
    <role>Producer</role>
    <type>Producer</type>
    <thumb>/var/lib/jellyfin/metadata/People/E/Emma Thomas/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Thomas Hayslip</name>
    <role>Executive Producer</role>
    <type>Producer</type>
  </actor>
  <actor>
    <name>Helen Medrano</name>
    <role>Associate Producer</role>
    <type>Producer</type>
  </actor>
  <actor>
    <name>Andy Thompson</name>
    <role>Co-Producer</role>
    <type>Producer</type>
  </actor>
  <actor>
    <name>Ivo Felt</name>
    <role>Line Producer</role>
    <type>Producer</type>
    <thumb>/var/lib/jellyfin/metadata/People/I/Ivo Felt/folder.jpg</thumb>
  </actor>
  <actor>
    <name>Per Henry Borch</name>
    <role>Line Producer</role>
    <type>Producer</type>
    <thumb>/var/lib/jellyfin/metadata/People/P/Per Henry Borch/folder.jpg</thumb>
  </actor>
  <id>tt6723592</id>
  <fileinfo>
    <streamdetails>
      <video>
        <codec>h264</codec>
        <micodec>h264</micodec>
        <bitrate>3976453</bitrate>
        <width>1920</width>
        <height>872</height>
        <aspect>240:109</aspect>
        <aspectratio>240:109</aspectratio>
        <framerate>23.976025</framerate>
        <scantype>progressive</scantype>
        <default>True</default>
        <forced>False</forced>
        <duration>149</duration>
        <durationinseconds>8984</durationinseconds>
      </video>
      <audio>
        <codec>ac3</codec>
        <micodec>ac3</micodec>
        <bitrate>384000</bitrate>
        <language>eng</language>
        <scantype>progressive</scantype>
        <channels>6</channels>
        <samplingrate>48000</samplingrate>
        <default>True</default>
        <forced>False</forced>
      </audio>
    </streamdetails>
  </fileinfo>
</movie>
"""
