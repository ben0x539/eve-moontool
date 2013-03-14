#!/usr/bin/env ruby

begin
  require 'net/https'

  class UserError < StandardError; end

  uri = URI.parse("https://adashboard.info/intel")
  req = Net::HTTP::Post.new(uri.path)
  req.set_form_data( { "Paste anything" => STDIN.read, "submit" => "new" } )

  ary = []
  ENV.each do |k, v|
    next unless k.start_with?('HTTP_EVE_')
    req[k[5..-1]] = v # pass header on to df
    ary << "#{k[9..-1].downcase.inspect}: #{v.inspect}" # return header to js
  end

  sock = Net::HTTP.new(uri.host, uri.port)
  sock.use_ssl = true
  sock.verify_mode = OpenSSL::SSL::VERIFY_NONE
  result = sock.start {|http| http.request(req)}

  case result.code
  when "200"
    raise UserError, "Posting dscan results: #{result.body}"
  when "303"
    location = result.header["Location"] #[-7..-1]
    if location.start_with?("/")
      location = "https://adashboard.info" + location
    end
    #raise UserError, "can't parse URL: #{result.header["Location"].inspect}" \
    #  unless location.match(/^[A-Za-z0-9]+$/)

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
