import requests
import xml.dom.minidom as minidom
url="https://na9.medrio.com/MedrioWeb/ws/ODMImportService.svc"
headers= {'content-type': 'application/soap+xml'}
body= """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:med="http://medrio.com">
   <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
      <wsa:Action soap:mustUnderstand="1">http://medrio.com/IODMImportService/SubmitODMImport</wsa:Action>
      <wsa:To soap:mustUnderstand="1">https://na9.medrio.com/MedrioWeb/ws/ODMImportService.svc</wsa:To>
   </soap:Header>
   <soap:Body>
      <med:SubmitODMImport>
         <med:file>
<ODM>
  <ClinicalData StudyOID="DS107E-06_DEV" MetadataVersionOID="1">
    <SubjectData SubjectKey="10102">
      <SiteRef LocationOID="001"/>
    </SubjectData>
  </ClinicalData>
</ODM></med:file>
         <med:apiKey>APIKEYHERE</med:apiKey>
      </med:SubmitODMImport>
   </soap:Body>
</soap:Envelope>"""

response = requests.post(url, data=body, headers=headers)
print(minidom.parseString(response.content).toprettyxml())
