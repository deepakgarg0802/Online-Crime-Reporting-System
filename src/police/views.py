from django.http import Http404
from django.shortcuts import render,get_object_or_404
from case.models import *
from .models import *
import urllib.request, json 
from django.db.models import Count
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout

from case.models import CaseCategory, CyberCaseCategories,Case, Witness

from citizen.models import Citizen
from .forms import UsersLoginForm,criminal_form

from home.models import AnonymousTip

from decouple import config

def login_view(request):

    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/police/dashboard")
    return render(request, "police/login.html", {"form": form})



def get_case_categories(request):
    if request.method == "GET" and request.is_ajax():
        case_category_qset= CaseCategory.objects.all()
        cyber_case_category_qset= CyberCaseCategories.objects.all()
        cyber_data =  serialize("json", cyber_case_category_qset)
        case_data =  serialize("json", case_category_qset)
        data = {
            "cyber_data": cyber_data,
            "case_data":case_data,
        }

        return HttpResponse(json.dumps(data), content_type='application/json')




def dashboard(request):
    if not request.user.is_authenticated() or not str(request.user.__class__.__name__)=="Police":
        raise Http404


    ward_object=request.user.ward

    total_cases_count=Case.objects.all().count()
    approved_cases_count=Case.objects.filter(approved=True).count()
    solved_cases_count=Case.objects.filter(solved=True).count()
    pending_cases_count=total_cases_count-approved_cases_count

    pqset=Police.objects.filter(ward=request.user.ward)

    cvqset={}
    d=CaseCategory.objects.all()
    cvsum=0
  
    
    for i in d:
        cvqset[i.name]=Case.objects.filter(case_categories=i).count()
        cvsum=cvsum+cvqset[i.name]

    cvsolved=Case.objects.filter(cyber_case_categories=None,solved=True).count()
    cysolved=Case.objects.filter(case_categories=None,solved=True).count()
    
    cyqset={}
    cysum=0
    d=CyberCaseCategories.objects.all()

    for i in d:
        cyqset[i.name]=Case.objects.filter(cyber_case_categories=i).count()
        cysum=cysum+cyqset[i.name]


    desig={
        'DGP': 'Director General of Police',
        'ADGP': 'Addl. Director General of Police',
        'IGP': 'Inspector General of Police',
        'DIGP': 'Deputy Inspector General of Police',
        'SPDCP': 'Superintendent of police Deputy Commissioner of Police(Selection Grade)',
        'SPDCPJ': 'Superintendent of police Deputy Commissioner of Police(Junior Management Grade)',
        'ASPADCP': 'Addl. Superintendent of police Addl.Deputy Commissioner of Police',
        'ASP': 'Assistant Superintendent of Police',
        'INSP': 'Inspector of Police',
        'SUB_INSP': 'Sub Inspector of Police.',
        'HVLDRM': 'Asst. Sub. Inspector/Havildar Major',
        'HVLDR': 'Havildar.',
        'LN': 'Lance Naik.',
        'CONS': 'Constable.',
        }
    res=[]
    for obj in pqset:
        res.append([obj.get_full_name(),desig[obj.designation]])




    context={
    "total_cases_count":total_cases_count,
    "approved_cases_count":approved_cases_count,
    "pending_cases_count":pending_cases_count,
    "solved_cases_count":solved_cases_count,
    "res":res,
    "ward_object":ward_object,
    "cvqset":cvqset,
    "cyqset":cyqset,
    "cvsum":cvsum,
    "cysum":cysum,
    "cvsolved":cvsolved,
    "cysolved":cysolved,
    



    }
    return render(request,'police/dashboard.html',context)


def cbcview(request,id=None):
    if not request.user.is_authenticated():
        raise Http404
    my_object = get_object_or_404(CaseCategory, pk=id)
    cases_qset=Case.objects.filter(case_categories=my_object )


    context={"my_object":my_object,"cases_qset":cases_qset}
    return render(request,'police/cases_by_cat.html',context)


def cybercbcview(request,id=None):
    if not request.user.is_authenticated():
        raise Http404
    my_cyber_object = get_object_or_404(CyberCaseCategories, pk=id)
    cyber_cases_qset=Case.objects.filter(cyber_case_categories=my_cyber_object )
    cyber_cases_qset=Case.objects.filter(cyber_case_categories=my_cyber_object)

    context={"my_object":my_cyber_object,"cases_qset":cyber_cases_qset}
    return render(request,'police/cases_by_cat.html',context)


from comment.models import Comment


def is_image(value):
    ref=['ANI', 'BMP', 'CAL', 'FAX', 'GIF', 'IMG', 'JBG', 'JPE', 'JPEG', 'JPG', 'MAC', 'PBM', 'PCD', 'PCX', 'PCT', 'PGM', 'PNG', 'PPM', 'PSD', 'RAS', 'TGA', 'TIFF', 'WMF']
    for i in ref:
        if(str(value).endswith(i.lower()) or str(value).endswith(i.upper())):
            return True
    return False





def is_video(value):
    ref=['.264', '.3G2', '.3GP', '.3GP2', '.3GPP', '.3GPP2', '.3MM', '.3P2', '.60D', '.787', '.890', '.AAF', '.AEC', '.AECAP', '.AEGRAPHIC', '.AEP', '.AEPX', '.AET', '.AETX', '.AJP', '.ALE', '.AM', '.AMC', '.AMV', '.AMX', '.ANIM', '.ANX', '.AQT', '.ARCUT', '.ARF', '.ASF', '.ASX', '.AVB', '.AVC', '.AVCHD', '.AVD', '.AVI', '.AVM', '.AVP', '.AVS', '.AVS', '.AVV', '.AWLIVE', '.AXM', '.AXV', '.BDM', '.BDMV', '.BDT2', '.BDT3', '.BIK', '.BIN', '.BIX', '.BMC', '.BMK', '.BNP', '.BOX', '.BS4', '.BSF', '.BU', '.BVR', '.BYU', '.CAMPROJ', '.CAMREC', '.CAMV', '.CED', '.CEL', '.CINE', '.CIP', '.CLK', '.CLPI', '.CMMP', '.CMMTPL', '.CMPROJ', '.CMREC', '.CMV', '.CPI', '.CPVC', '.CREC', '.CST', '.CVC', '.CX3', '.D2V', '.D3V', '.DASH', '.DAT', '.DAV', '.DB2', '.DCE', '.DCK', '.DCR', '.DCR', '.DDAT', '.DIF', '.DIR', '.DIVX', '.DLX', '.DMB', '.DMSD', '.DMSD3D', '.DMSM', '.DMSM3D', '.DMSS', '.DMX', '.DNC', '.DPA', '.DPG', '.DREAM', '.DSY', '.DV', '.DV-AVI', '.DV4', '.DVDMEDIA', '.DVR', '.DVR-MS', '.DVX', '.DXR', '.DZM', '.DZP', '.DZT', '.EDL', '.EVO', '.EVO', '.EXO', '.EYE', '.EYETV', '.EZT', '.F4F', '.F4M', '.F4P', '.F4V', '.FBR', '.FBR', '.FBZ', '.FCARCH', '.FCP', '.FCPROJECT', '.FFD', '.FFM', '.FLC', '.FLH', '.FLI', '.FLIC', '.FLV', '.FLX', '.FPDX', '.FTC', '.FVT', '.G2M', '.G64', '.G64X', '.GCS', '.GFP', '.GIFV', '.GL', '.GOM', '.GRASP', '.GTS', '.GVI', '.GVP', '.GXF', '.H264', '.HDMOV', '.HDV', '.HKM', '.IFO', '.IMOVIELIBRARY', '.IMOVIEMOBILE', '.IMOVIEPROJ', '.IMOVIEPROJECT', '.INP', '.INT', '.IRCP', '.IRF', '.ISM', '.ISMC', '.ISMCLIP', '.ISMV', '.IVA', '.IVF', '.IVR', '.IVS', '.IZZ', '.IZZY', '.JDR', '.JMV', '.JNR', '.JSS', '.JTS', '.JTV', '.K3G', '.KDENLIVE', '.KMV', '.KTN', '.LREC', '.LRV', '.LSF', '.LSX', '.LVIX', '.M15', '.M1PG', '.M1V', '.M21', '.M21', '.M2A', '.M2P', '.M2T', '.M2TS', '.M2V', '.M4E', '.M4U', '.M4V', '.M75', '.MANI', '.META', '.MGV', '.MJ2', '.MJP', '.MJPEG', '.MJPG', '.MK3D', '.MKV', '.MMV', '.MNV', '.MOB', '.MOD', '.MODD', '.MOFF', '.MOI', '.MOOV', '.MOV', '.MOVIE', '.MP21', '.MP21', '.MP2V', '.MP4', '.MP4.INFOVID', '.MP4V', '.MPE', '.MPEG', '.MPEG1', '.MPEG2', '.MPEG4', '.MPF', '.MPG', '.MPG2', '.MPG4', '.MPGINDEX', '.MPL', '.MPL', '.MPLS', '.MPROJ', '.MPSUB', '.MPV', '.MPV2', '.MQV', '.MSDVD', '.MSE', '.MSH', '.MSWMM', '.MT2S', '.MTS', '.MTV', '.MVB', '.MVC', '.MVD', '.MVE', '.MVEX', '.MVP', '.MVP', '.MVY', '.MXF', '.MXV', '.MYS', '.N3R', '.NCOR', '.NFV', '.NSV', '.NTP', '.NUT', '.NUV', '.NVC', '.OGM', '.OGV', '.OGX', '.ORV', '.OSP', '.OTRKEY', '.PAC', '.PAR', '.PDS', '.PGI', '.PHOTOSHOW', '.PIV', '.PJS', '.PLAYLIST', '.PLPROJ', '.PMF', '.PMV', '.PNS', '.PPJ', '.PREL', '.PRO', '.PRO4DVD', '.PRO5DVD', '.PROQC', '.PRPROJ', '.PRTL', '.PSB', '.PSH', '.PSSD', '.PVA', '.PVR', '.PXV', '.QT', '.QTCH', '.QTINDEX', '.QTL', '.QTM', '.QTZ', '.R3D', '.RCD', '.RCPROJECT', '.RCREC', '.RCUT', '.RDB', '.REC', '.RM', '.RMD', '.RMD', '.RMP', '.RMS', '.RMV', '.RMVB', '.ROQ', '.RP', '.RSX', '.RTS', '.RTS', '.RUM', '.RV', '.RVID', '.RVL', '.SAN', '.SBK', '.SBT', '.SBZ', '.SCC', '.SCM', '.SCM', '.SCN', '.SCREENFLOW', '.SDV', '.SEC', '.SEC', '.SEDPRJ', '.SEQ', '.SFD', '.SFERA', '.SFVIDCAP', '.SIV', '.SMI', '.SMI', '.SMIL', '.SMK', '.SML', '.SMV', '.SNAGPROJ', '.SPL', '.SQZ', '.SRT', '.SSF', '.SSM', '.STL', '.STR', '.STX', '.SVI', '.SWF', '.SWI', '.SWT', '.TDA3MT', '.TDT', '.TDX', '.THEATER', '.THP', '.TID', '.TIVO', '.TIX', '.TOD', '.TP', '.TP0', '.TPD', '.TPR', '.TREC', '.TRP', '.TS', '.TSP', '.TTXT', '.TVLAYER', '.TVRECORDING', '.TVS', '.TVSHOW', '.USF', '.USM', '.V264', '.VBC', '.VC1', '.VCPF', '.VCR', '.VCV', '.VDO', '.VDR', '.VDX', '.VEG', '.VEM', '.VEP', '.VF', '.VFT', '.VFW', '.VFZ', '.VGZ', '.VID', '.VIDEO', '.VIEWLET', '.VIV', '.VIVO', '.VIX', '.VLAB', '.VMLF', '.VMLT', '.VOB', '.VP3', '.VP6', '.VP7', '.VPJ', '.VR', '.VRO', '.VS4', '.VSE', '.VSP', '.VTT', '.W32', '.WCP', '.WEBM', '.WFSP', '.WGI', '.WLMP', '.WM', '.WMD', '.WMMP', '.WMV', '.WMX', '.WOT', '.WP3', '.WPL', '.WSVE', '.WTV', '.WVE', '.WVM', '.WVX', '.WXP', '.XEJ', '.XEL', '.XESC', '.XFL', '.XLMV', '.XML', '.XMV', '.XVID', '.Y4M', '.YOG', '.YUV', '.ZEG', '.ZM1', '.ZM2', '.ZM3', '.ZMV']

    for i in ref:
        if(str(value).endswith(i.lower()) or str(value).endswith(i.upper())):
            return True
    return False


def is_audio(value):
    ref=['.3GA', '.4MP', '.5XB', '.5XE', '.5XS', '.669', '.8SVX', '.A2B', '.A2I', '.A2M', '.AA', '.AA3', '.AAC', '.AAX', '.AB', '.ABC', '.ABM', '.AC3', '.ACD', '.ACD-BAK', '.ACD-ZIP', '.ACM', '.ACP', '.ACT', '.ADG', '.ADT', '.ADTS', '.ADV', '.AFC', '.AGM', '.AGR', '.AIF', '.AIFC', '.AIFF', '.AIMPPL', '.AKP', '.ALC', '.ALL', '.ALS', '.AMF', '.AMR', '.AMS', '.AMS', '.AMXD', '.AMZ', '.ANG', '.AOB', '.APE', '.APL', '.ARIA', '.ARIAX', '.ASD', '.AT3', '.AU', '.AUD', '.AUP', '.AVASTSOUNDS', '.AY', '.B4S', '.BAND', '.BAP', '.BDD', '.BIDULE', '.BNK', '.BRSTM', '.BUN', '.BWF', '.BWG', '.BWW', '.CAF', '.CAFF', '.CDA', '.CDDA', '.CDLX', '.CDO', '.CDR', '.CEL', '.CFA', '.CGRP', '.CIDB', '.CKB', '.CKF', '.CONFORM', '.COPY', '.CPR', '.CPT', '.CSH', '.CTS', '.CWB', '.CWP', '.CWS', '.CWT', '.DCF', '.DCM', '.DCT', '.DEWF', '.DF2', '.DFC', '.DFF', '.DIG', '.DIG', '.DLS', '.DM', '.DMC', '.DMF', '.DMSA', '.DMSE', '.DRA', '.DRG', '.DS', '.DS2', '.DSF', '.DSM', '.DSS', '.DTM', '.DTS', '.DTSHD', '.DVF', '.DWD', '.EFA', '.EFE', '.EFK', '.EFQ', '.EFS', '.EFV', '.EMD', '.EMP', '.EMX', '.ESPS', '.EXPRESSIONMAP', '.EXS', '.F2R', '.F32', '.F3R', '.F4A', '.F64', '.FDP', '.FEV', '.FLAC', '.FLM', '.FLP', '.FLP', '.FPA', '.FPR', '.FRG', '.FSB', '.FSC', '.FSM', '.FTM', '.FTM', '.FTMX', '.FZF', '.FZV', '.G721', '.G723', '.G726', '.GBPROJ', '.GBS', '.GIG', '.GP5', '.GPBANK', '.GPK', '.GPX', '.GROOVE', '.GSF', '.GSFLIB', '.GSM', '.H0', '.H4B', '.H5B', '.H5E', '.H5S', '.HBE', '.HDP', '.HMA', '.HSB', '.IAA', '.ICS', '.IFF', '.IGP', '.IGR', '.IMP', '.INS', '.INS', '.ISMA', '.ITI', '.ITLS', '.ITS', '.JAM', '.JSPF', '.K26', '.KAR', '.KFN', '.KMP', '.KOZ', '.KOZ', '.KPL', '.KRZ', '.KSC', '.KSF', '.KT3', '.L', '.LA', '.LOF', '.LOGIC', '.LOGICX', '.LSO', '.LWV', '.M3U', '.M3U8', '.M4A', '.M4B', '.M4P', '.M4R', '.M5P', '.MA1', '.MBR', '.MDC', '.MDR', '.MED', '.MGV', '.MID', '.MIDI', '.MINIGSF', '.MINIPSF', '.MINIUSF', '.MKA', '.MMF', '.MMLP', '.MMM', '.MMP', '.MMPZ', '.MO3', '.MOD', '.MOGG', '.MP2', '.MP3', '.MPA', '.MPC', '.MPDP', '.MPGA', '.MPU', '.MSCX', '.MSCZ', '.MSV', '.MT2', '.MTE', '.MTF', '.MTI', '.MTM', '.MTP', '.MTS', '.MUI', '.MUS', '.MUS', '.MUS', '.MUSX', '.MUX', '.MX3', '.MX4', '.MX5', '.MX5TEMPLATE', '.MXL', '.MXMF', '.MYR', '.NARRATIVE', '.NBS', '.NCW', '.NKB', '.NKC', '.NKI', '.NKM', '.NKS', '.NKX', '.NML', '.NMSV', '.NOTE', '.NPL', '.NRA', '.NRT', '.NSA', '.NTN', '.NVF', '.NWC', '.OBW', '.ODM', '.OFR', '.OGA', '.OGG', '.OKT', '.OMA', '.OMF', '.OMG', '.OMX', '.OPUS', '.OTS', '.OVE', '.OVW', '.OVW', '.PAC', '.PANDORA', '.PBF', '.PCA', '.PCAST', '.PCG', '.PEAK', '.PEK', '.PHO', '.PHY', '.PK', '.PKF', '.PLA', '.PLS', '.PLY', '.PNA', '.PNO', '.PPC', '.PPCX', '.PRG', '.PSF', '.PSF1', '.PSF2', '.PSM', '.PSY', '.PTCOP', '.PTF', '.PTM', '.PTS', '.PTT', '.PTX', '.PTXT', '.PVC', '.QCP', '.R1M', '.RA', '.RAM', '.RAW', '.RAX', '.RBS', '.RBS', '.RCY', '.REX', '.RFL', '.RGRP', '.RIP', '.RMI', '.RMJ', '.RMX', '.RNG', '.RNS', '.ROL', '.RSN', '.RSO', '.RTA', '.RTI', '.RTS', '.RVX', '.RX2', '.S3I', '.S3M', '.S3Z', '.SAF', '.SAP', '.SBG', '.SBI', '.SC2', '.SCS11', '.SD', '.SD', '.SD2', '.SD2F', '.SDAT', '.SDS', '.SDT', '.SEQ', '.SES', '.SESX', '.SF2', '.SFAP0', '.SFK', '.SFL', '.SFPACK', '.SFS', '.SFZ', '.SGP', '.SHN', '.SIB', '.SLP', '.SLX', '.SMA', '.SMF', '.SMP', '.SMP', '.SMPX', '.SND', '.SND', '.SND', '.SNG', '.SNG', '.SNS', '.SONG', '.SOU', '.SPPACK', '.SPRG', '.SPX', '.SSEQ', '.SSEQ', '.SSM', '.SSND', '.STAP', '.STM', '.STX', '.STY', '.SVD', '.SVX', '.SWA', '.SXT', '.SYH', '.SYN', '.SYW', '.SYX', '.TAK', '.TAK', '.TD0', '.TG', '.TOC', '.TRAK', '.TTA', '.TXW', '.U', '.UAX', '.ULT', '.UNI', '.USF', '.USFLIB', '.UST', '.UW', '.UWF', '.VAG', '.VAP', '.VB', '.VC3', '.VDJ', '.VGM', '.VGZ', '.VIP', '.VLC', '.VMD', '.VMF', '.VMF', '.VMO', '.VOC', '.VOX', '.VOXAL', '.VPL', '.VPM', '.VPW', '.VQF', '.VRF', '.VSQ', '.VSQX', '.VTX', '.VYF', '.W01', '.W64', '.WAV', '.WAVE', '.WAX', '.WEM', '.WFB', '.WFD', '.WFM', '.WFP', '.WMA', '.WOW', '.WPK', '.WPP', '.WPROJ', '.WRK', '.WTPL', '.WTPT', '.WUS', '.WUT', '.WV', '.WVC', '.WVE', '.WWU', '.XA', '.XA', '.XFS', '.XM', '.XMF', '.XMU', '.XRNS', '.XSP', '.XSPF', '.YOOKOO', '.ZPA', '.ZPL', '.ZVD']
    for i in ref:
        if(str(value).endswith(i.lower()) or str(value).endswith(i.upper())):
            return True
    return False




def get_last(value):
    spam = value.split('/')[-1]         # assume value be /python/web-scrapping
                                        # spam would be 'web-scrapping'
    spam = ' '.join(spam.split('-'))    # now spam would be 'web scrapping'
    return spam



def is_docu(value):
    ref=['ABW', 'WRF', 'WRI', 'XHTML', 'XML', 'PDF', 'HTML', 'HWP', 'QUOX', 'TeX', 'AWW', 'ACL', 'SXW', 'Amigaguide', 'NB', 'CWK', 'MCW', 'DOT', 'HWPML', 'LWP', 'Texinfo', 'DOTX', 'RTF', 'DOC', 'CSV', 'FDX', 'WPD', 'ODM', 'ANS', 'ODT', 'TXT', 'WPS', 'WPT', 'PAGES', 'PAP', 'AFP', 'SDW', 'NBP', 'UOF', 'DOCX', 'OTT', 'CELL', 'ODS', 'VC', 'OTS', 'QPW', 'XLS', 'XLSB', 'CSV', 'XLW', 'XLSM', 'XLSX', 'WK4', 'XLR', 'SDC', 'XLT', 'SXC', 'XLK', 'XLTM', 'WK3', 'STC', 'SLK', 'AWS', 'WKS', 'WKS', 'WQ1', 'WK1', 'NBP', 'ODP', 'STI', 'SXI', 'OTP', 'SHW', 'NB', 'SDD', 'POT', 'PPS', 'PRZ', 'KEY,', 'KEYNOTE', 'PPT', 'SLP', 'WATCH', 'SSPSS', 'PPTX']
    for i in ref:
        if(str(value).endswith(i.lower()) or str(value).endswith(i.upper())):
            return True
    return False


def case_detail(request,id=None,approved=None):
    if not request.user.is_authenticated():
        raise Http404
    app=approved
    comments = Comment.objects.filter(case = id)
    my_object = get_object_or_404(Case, id=id)
    if app=='1':
        my_object.approved=True
        print("yppppppppppppppp")
        my_object.save()
    wqset=Witness.objects.filter(case=my_object)
    ward_object=request.user.ward
    police_id = request.user.id
    files = my_object.evidence_set.all()
    imglist={}
    vidlist={}
    audlist={}
    doculist={}
    others={}
    for i in files:
        

        if is_image(get_last(i.evidence.name)):
            imglist[get_last(i.evidence.name)]=i.evidence.url


        elif is_audio(get_last(i.evidence.name)):
            audlist[get_last(i.evidence.name)]=i.evidence.url
        
        elif is_video(get_last(i.evidence.name)):
            vidlist[get_last(i.evidence.name)]=i.evidence.url
        
        elif is_docu(get_last(i.evidence.name)):
            doculist[get_last(i.evidence.name)]=i.evidence.url

        else:

            others[get_last(i.evidence.name)]=i.evidence.url


        
    

    print(others)
    context={"my_object":my_object,"wqset":wqset, "ward_object": ward_object, "police_id": police_id, "comments": comments,'files':files,"imglist":imglist,"vidlist":vidlist,"audlist":audlist,"doculist":doculist,"others":others}
    return render(request,'police/case_detail.html',context)

def atip_detail(request,id=None):
    if not request.user.is_authenticated():
        raise Http404
    my_object = get_object_or_404(AnonymousTip, id=id)
    
    context={"my_object":my_object}
    return render(request,'police/atip_detail.html',context)

def b(b_id):
    try:
        string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp/%s?client_id=%s" % (str(b_id),config('client_id'))
        with urllib.request.urlopen(string) as url:
            data=json.loads(url.read().decode())
        data=data['hof_Details']
        return data
    except:
        return None




def person_detail_view(request,id=None):
    if not request.user.is_authenticated():
        raise Http404

    # user = get_object_or_404(Citizen,id=id)
    # b_id = user.bhamashah
    b_id=id
    photo_flag=1
    detail_flag=1
    d64={}
    data={}
 
    data = b(b_id)
    print(data)

    if data is None:
        detail_flag=0


    try:

        string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofMembphoto/%s/%s?client_id=%s" % (str(data['BHAMASHAH_ID']),str(data['M_ID']),config('client_id'))  
        with urllib.request.urlopen(string) as url:
            d64=json.loads(url.read().decode())
        d64=d64["hof_Photo"]["PHOTO"]
    except:
        photo_flag=0

       

    context={

        "data":data,
        "d64":d64,
        "detail_flag":detail_flag,
        "photo_flag":photo_flag,


    }
  






    return render(request,'police/citizen_detail.html',context)



def police_logout(request):
    logout(request)

    return redirect("/")



def create_criminal_details(request):
    form=criminal_form(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return redirect("/police/criminal_directory")
    return render(request, "police/cdform.html",{"form" : form,})



def atips(request):
    if not request.user.is_authenticated():
        raise Http404
    aqset = AnonymousTip.objects.all()
    context={"aqset":aqset}
    return render(request,'police/atips.html',context)

