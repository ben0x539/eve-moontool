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
    raise UserError, "can't parse URL: #{result.header["Loction"].inspect}" \
      unless location.match(/^[A-Za-z0-9]+$/)

    ary = []
    ENV.each do |k, v|
      next unless k.start_with?('HTTP_EVE_')
      ary << "#{k[9..-1].downcase.inspect}: #{v.inspect}"
    end

    ary << "\"token\": #{location.inspect}"
    result = ary.join(',')
    print "Status: 200 OK\r\nContent-type: text/plain\r\n\r\n{"
    print result
    print "}"
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
