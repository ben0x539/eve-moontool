#!/usr/bin/env ruby

begin
  ary = []
  ENV.each do |k, v|
    next unless k.start_with?('HTTP_EVE_')
    ary << "#{k[9..-1].downcase.inspect}: #{v.inspect}"
  end

  result = ary.join(',')
  print "Status: 200 OK\r\nContent-type: text/plain\r\n\r\n{"
  print result
  print "}"
rescue Exception => e
  print "Status: 500 Internal Server Error\r\nContent-type: text/plain\r\n\r\n"
  puts "#{e.class}: #{e.inspect}"
  puts "#{e.backtrace}"
end
