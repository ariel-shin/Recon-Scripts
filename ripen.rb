#!/usr/bin/env ruby
require 'net/http'
require 'json'

if ARGV.length < 2
  puts "Usage: ripen.rb ip-filename output-filename.csv"
  exit
end

filename = ARGV[0].chomp
csvFileName = ARGV[1].chomp

#check if input file exists
if( File.exists?( filename ) )
	puts "Working on #{filename}"
else
	puts "#{filename} doesn't exist..."
end

#check if output file exists
if( File.exists?( csvFileName ) || File.exists?( csvFileName + ".csv" ) )
	puts "#{csvFileName} exists... Please choose a different name"
	exit
elsif ( !csvFileName.end_with?( ".csv" ))
	csvFileName << ".csv"
	puts "Appending .csv to filename --> #{csvFileName}"
else
	puts "Outputting to: #{csvFileName}"
end

ipArray = Array.new
file = File.open( filename, 'rb' )
file.each do |line|
	if( line.match( /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/ ) )
		ipArray << line.chomp 
	end
end
file.close

csvFile = File.open( csvFileName, 'ab' )

#add header
header = String.new("ip, inetnum,netname,descr,country,status,mnt-by,source,extra1,extra2,extra3,extra4,reverseDNS\n")
csvFile.write( header )

def callRIPE(ip, csvFile)
	urlResource = 'https://stat.ripe.net/data/whois/data.json?resource=' + ip
	uri = URI(urlResource)
	response = Net::HTTP.get(uri)
	data = JSON.parse(response)

	# iterate through the records
	csvString = String.new
	csvString.clear
	csvString << "#{ip},"
	result = data['data']['records'][0]
	result.each do |hash|
		csvString << "#{hash['value']},"
	end

	#get reverse dns
	dnsResource = 'https://stat.ripe.net/data/reverse-dns/data.json?resource=' + ip
	uri2 = URI(dnsResource)
	response2 = Net::HTTP.get(uri2)
	data2 = JSON.parse(response2)
	result2 = data2['data']['delegations'][0][0]['value']
	csvString << "#{result2}"

	csvString << "#{csvString}\n"
	csvFile.write( csvString )
end

ipArray.each do |ip|
	puts "Working on IP: #{ip}"
	callRIPE(ip, csvFile)
end

csvFile.close
