#!/usr/bin/env ruby

begin
  require 'net/http'

  class UserError < StandardError; end

  result = Net::HTTP.post_form(
    URI.parse("http://raynor.cl/eve/formRecive.php"),
    { "scanData" => STDIN.read }
  )

  case result.code
  when "200"
    raise UserError, "Posting dscan results: #{result.body}"
  when "302"
    location = result.header["Location"][-7..-1]
    print "Status: 200 OK\r\nContent-type: text/plain\r\n\r\n"
    print location
  else
    raise UserError, "Posting dscan results: #{result.msg}"
  end

rescue UserError => e
  print "Status: 500 Internal Server Error\r\nContent-type: text/plain\r\n\r\n"
  puts e
rescue Exception => e
  print "Status: 500 Internal Server Error\r\nContent-type: text/plain\r\n\r\n"
  puts "#{e.class}: #{e.inspect}"
  puts "#{e.backtrace}"
end
