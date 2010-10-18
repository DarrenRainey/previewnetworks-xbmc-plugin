"""
    Plugin for streaming Preview network
"""

# main imports
import sys
import os
import xbmc
import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import cgi
import socket
import xbmcaddon
 
# plugin constants
__plugin__ = "Preview networks"
__author__ = "nmazz64"
__url__ = "http://code.google.com/p/previewnetworks-xbmc-plugin"
__svn_url__ = "http://previewnetworks-xbmc-plugin.googlecode.com/files"
__useragent__ = "QuickTime/7.6.5 (qtver=7.6.5;os=Windows NT 5.1Service Pack 3)"
__version__ = "2.0.0"
__svn_revision__ = "$Revision: 1$"
__XBMC_Revision__ = "31632"

url_source=None

def check_compatible():
    try:
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
#    xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
#    xbmc.log( "     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    # if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        xbmcgui.Dialog().ok( "%s - %s: %s" % ( __plugin__, xbmc.getLocalizedString( 30700 ), __version__, ), xbmc.getLocalizedString( 30701 ) % ( __plugin__, ), xbmc.getLocalizedString( 30702 ) % ( __XBMC_Revision__, ), xbmc.getLocalizedString( 30703 ) )
    #return result
    return ok

def categories(root):
    icona = os.path.join(os.getcwd(),'resources','images','list.png')
    new_icon = os.path.join(os.getcwd(), 'resources','images', 'new.png')
    now_icon = os.path.join(os.getcwd(), 'resources','images', 'now.png')
    next_icon = os.path.join(os.getcwd(), 'resources','images', 'next.png')
    genre_icon = os.path.join(os.getcwd(), 'resources','images', 'genre.png')
    search_icon = os.path.join(os.getcwd(), 'resources','images', 'search.png')
    #baseurl="http://%s.feed.previewnetworks.com/v3.1/%s/"
    baseurl="http://%s.hdplus.previewnetworks.com/v3.1/%s/"

    if root:
        addDir(Addon.getLocalizedString(30301),baseurl+'now-90/%s',1,now_icon)
        addDir(Addon.getLocalizedString(30302),baseurl+'coming-90/%s',2,next_icon)
        addDir(Addon.getLocalizedString(30303),baseurl+'newest-90/%s',3,new_icon)
        addDir(Addon.getLocalizedString(30300),'genre:',0,genre_icon)
        addDir(Addon.getLocalizedString(30340),baseurl+'search-20/%s/?search_field=product_title&search_query=%s',99,search_icon) 
    else:
        addDir(Addon.getLocalizedString(30304),baseurl+'CinemaAction/%s',10,icona)
        addDir(Addon.getLocalizedString(30305),baseurl+'CinemaAdventure/%s',11,icona)
        addDir(Addon.getLocalizedString(30306),baseurl+'CinemaAnimation/%s',12,icona)
        addDir(Addon.getLocalizedString(30307),baseurl+'CinemaBiography/%s',13,icona)
        addDir(Addon.getLocalizedString(30308),baseurl+'CinemaComedy/%s',14,icona)
        addDir(Addon.getLocalizedString(30309),baseurl+'CinemaCrime/%s',15,icona)
        addDir(Addon.getLocalizedString(30310),baseurl+'CinemaDocumentary/%s',16,icona)
        addDir(Addon.getLocalizedString(30311),baseurl+'CinemaDrama/%s',17,icona)
        addDir(Addon.getLocalizedString(30312),baseurl+'CinemaFamily/%s',18,icona)
        addDir(Addon.getLocalizedString(30313),baseurl+'CinemaFantasy/%s',19,icona)
        addDir(Addon.getLocalizedString(30314),baseurl+'CinemaFilmNoir/%s',20,icona)
        addDir(Addon.getLocalizedString(30315),baseurl+'CinemaGameShow/%s',21,icona)
        addDir(Addon.getLocalizedString(30316),baseurl+'CinemaHistory/%s',22,icona)
        addDir(Addon.getLocalizedString(30317),baseurl+'CinemaHorror/%s',23,icona)
        addDir(Addon.getLocalizedString(30318),baseurl+'CinemaMusic/%s',24,icona)
        addDir(Addon.getLocalizedString(30319),baseurl+'CinemaMusical/%s',25,icona)
        addDir(Addon.getLocalizedString(30320),baseurl+'CinemaMystery/%s',26,icona)
        addDir(Addon.getLocalizedString(30321),baseurl+'CinemaNews/%s',27,icona)
        addDir(Addon.getLocalizedString(30322),baseurl+'CinemaRealityTV/%s',28,icona)
        addDir(Addon.getLocalizedString(30323),baseurl+'CinemaRomance/%s',29,icona)
        addDir(Addon.getLocalizedString(30324),baseurl+'CinemaSciFi/%s',30,icona)
        addDir(Addon.getLocalizedString(30325),baseurl+'CinemaShort/%s',31,icona)
        addDir(Addon.getLocalizedString(30326),baseurl+'CinemaSport/%s',32,icona)
        addDir(Addon.getLocalizedString(30327),baseurl+'CinemaTalkShow/%s',33,icona)
        addDir(Addon.getLocalizedString(30328),baseurl+'CinemaThriller/%s',34,icona)
        addDir(Addon.getLocalizedString(30329),baseurl+'CinemaWar/%s',35,icona)
        addDir(Addon.getLocalizedString(30330),baseurl+'CinemaWestern/%s',36,icona)
        addDir(Addon.getLocalizedString(30331),baseurl+'CinemaChildrenMovie/%s',37,icona)


def addDir(name,url,item,iconimage,parametri={},info={}):
    standardParams={'url':url,'item':item}
    parametri.update(standardParams)
    u=sys.argv[0]+"?"+urllib.urlencode(parametri)
    ok=True 
    info.update({ "Titolo": name })
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage) 
    liz.setInfo( type="Video", infoLabels=info ) 
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True) 
    return ok

def get(params,name):
    return params[name][0]

url_source=None
name=None
item=None

Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )
BASE_CURRENT_SOURCE_PATH = xbmc.translatePath( Addon.getAddonInfo( "Profile" ) )

if sys.argv[ 2 ] == "":
    if ( check_compatible() ) == False:
        Return
    else:
        categories(True)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif ( __name__ == "__main__" ):
    if ( sys.argv[ 2 ].startswith( "?url" ) ):
        paramstring=sys.argv[2]
        if len(paramstring)>0 :
            params=cgi.parse_qs(paramstring[ 1 : ],True)
            item=str(get(params,"item"))
            if item == '0':
                categories(False)
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
            else:
                url_source=get(params,"url")
                import resources.lib.trailers as plugin
                plugin.Main(url_source,item)
                del plugin
    elif ( sys.argv[ 2 ].startswith( "?Fetch_Showtimes" ) ):
        import resources.lib.showtimes as showtimes
        s = showtimes.GUI( "plugin-AMTII-showtimes.xml", os.getcwd(), "default" )
        del s
    elif ( sys.argv[ 2 ].startswith( "?Download_Trailer" ) ):
        import resources.lib.download as download
        download.Main()
    elif ( sys.argv[ 2 ].startswith( "?OpenSettings" ) ):
        xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) ).openSettings()
        xbmc.executebuiltin( "Container.Refresh" )
