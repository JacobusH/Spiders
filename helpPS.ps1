# cleanup
 $csvToEdit = "crawltest.csv"
(Get-Content -Raw $csvToEdit) -replace '^sqlStmt(\r\n)*"', '' | Set-Content $csvToEdit # get rid of dictionary key from python
(Get-Content -Raw $csvToEdit) -replace '^"', '' | Set-Content $csvToEdit # get rid of beginning quote
###(Get-Content -Raw $csvToEdit) -replace '(?<!^)\r\n', '<br/>' | Set-Content $csvToEdit # get rid of encoded line breaks
(Get-Content -Raw $csvToEdit) -replace '(<br/>)+insert', 'insert' | Set-Content $csvToEdit # clean up beginning
(Get-Content -Raw $csvToEdit) -replace '^\r\n$', '' | Set-Content $csvToEdit # clean up single lines
(Get-Content $csvToEdit) -replace 'getUtcDate.*?$', 'getUtcDate())' | Set-Content $csvToEdit # clean up end again, NOTE no -raw on this one
