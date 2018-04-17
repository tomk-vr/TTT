import gcred
import httplib2

from apiclient import discovery

class Sheet(gcred.GCredentials):
    """Google sheet client"""

    SHEETID = '1Jym0-RUPbbfhDv2Batg1LUFoOiVgQD_4fZdFlk6MLr8'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'sheetId' in kwargs:
            self.SHEETID = kwargs['sheetId']
        http = self.credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    def get_interval(self, **kwargs):
        if 'range' in kwargs:
            rangeName = kwargs['range']
        else:
            rangeName = 'Ore'

        if 'silent' in kwargs:
            sil = kwargs['silent']
        else:
            sil = True

        result = self.service.spreadsheets().values().get(spreadsheetId=self.SHEETID, range=rangeName).execute()
        values = result.get('values', [])

        if sil :
            return values

        if not values:
            print('No data found.')
        else:
            for row in values:
                for ii in range(0,len(row)):
                    try:
                        print(row[ii], '  ', end='')
                    except IndexError:
                        print('EMPTY   ')
                print('')
        return values

    def update_sheet(self, sheet, year, month, val):
        values = self.get_interval(range=sheet)
        if not values: 
            return

        #update first line if year is not present
        if year not in values[0]:
            nrow = values[0] + [year]
            nvalues = [
                nrow,
            ]
            body = {
                'values': nvalues
            }

            rr = sheet + '!A1'
            result = self.service.spreadsheets().values().update(
                valueInputOption='USER_ENTERED', spreadsheetId=self.SHEETID, range=rr, body=body).execute()

        #update month line
        nrow = values[month] + val
        print(nrow)
        nvalues = [
            nrow,
        ]
        body = {
            'values': nvalues
        }

        rr = sheet + '!A' + str(month+1)
        result = self.service.spreadsheets().values().update(
            valueInputOption='USER_ENTERED', spreadsheetId=self.SHEETID, range=rr, body=body).execute()