$urls = @{}
$csvToEdit = "crawlyNoExamples.csv"

# # # # run sitecrawler script to get urls
scrapy crawl sitecrawly -o $csvToEdit

# # # # reset iis because of memory leak
Start-Process "iisreset.exe" -NoNewWindow -Wait

# # # # get rid of double quotes because python is dumb
(Get-Content $csvToEdit) -replace '"', '' | Set-Content $csvToEdit

# # # # replace python dict key with csv headers
(Get-Content $csvToEdit) -replace '^BLEHOUTPUT$', 'Origin, Inside' | Set-Content $csvToEdit

# get unique urls from .csv
$csv = Import-Csv $csvToEdit
$csv.Origin | ForEach-Object {
    If ($urls.Keys -notcontains $_) {
      $urls.Add($_, $false)
    }
}
$csv.Inside | ForEach-Object {
    If ($urls.Keys -notcontains $_) {
      $urls.Add($_, $false)
    }
}

# # # # feed unique urls into our doc crawler script, reset iis after every 15
$i = 0
foreach ($h in $urls.GetEnumerator()) {
    if($i++ % 15 -ne 0) {
      scrapy crawl simpleSpidy -a currentUrl=$($h.Name) -o newCrawly.csv
    } 
    else {
      Start-Process "iisreset.exe" -NoNewWindow -Wait
    }
}

# cleanup
 $csvToEdit = "newCrawly.csv"
(Get-Content -Raw $csvToEdit) -replace '(?ms)^sqlStmt(\r\n)*"', '' | Set-Content $csvToEdit # get rid of dictionary key from python
(Get-Content -Raw $csvToEdit) -replace '(?ms)^"', '' | Set-Content $csvToEdit # get rid of beginning quote
### (Get-Content -Raw $csvToEdit) -replace '(?<!^)\r\n', '<br/>' | Set-Content $csvToEdit # get rid of encoded line breaks ### puts br in table...
### (Get-Content -Raw $csvToEdit) -replace '(<br/>)+insert', 'insert' | Set-Content $csvToEdit # clean up beginning ### not replacing brs anymore
(Get-Content -Raw $csvToEdit) -replace '(?ms)^\r\n$', '' | Set-Content $csvToEdit # clean up single lines
(Get-Content $csvToEdit) -replace '(?ms)getUtcDate.*?$', 'getUtcDate())' | Set-Content $csvToEdit # clean up end again, NOTE no -raw on this one

# Now run this all in the database
# # # Invoke-sqlcmd -ServerInstance "devweb06" -Database "ProjectInsightWebsite" -InputFile "fullCrawly.csv"

# delete files so it be run again later
# # # Remove-Item –path "fullCrawly.csv"
# # # Remove-Item –path "crawlyNoExamples_2.csv"


#### TODO LATER:
# # # # make async mem check functions so my computer doesn't freeze...
# # # $scriptBlock = {
# # #   scrapy crawl sitecrawly -o crawlyNoExamples_2.csv
# # # }
# # # $scriptBlockReset = {
# # #   [decimal]$thresholdspace = 10
# # #   $tableFragment= Get-WMIObject  -ComputerName $computers Win32_LogicalDisk | Select-Object __SERVER, DriveType, VolumeName, Name, @{n='Size (Gb)' ;e={"{0:n2}" -f ($_.size/1gb)}},@{n='FreeSpace (Gb)';e={"{0:n2}" -f ($_.freespace/1gb)}}, @{n='PercentFree';e={"{0:n2}" -f ($_.freespace/$_.size*100)}} | Where-Object {$_.DriveType -eq 3 -and [decimal]$_.PercentFree -lt [decimal]$thresholdspace}
  
# # #   Suspend-Job -ScriptBlock $scriptBlock -Wait
# # #   Start-Process "iisreset.exe" -NoNewWindow -Wait
# # #   Resume-Job -ScriptBlock $scriptBlock
# # # }

# # # Start-Job -ScriptBlock $scriptBlock
# # # Start-Job -ScriptBlock $scriptBlockReset
