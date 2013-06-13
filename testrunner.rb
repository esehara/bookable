watch('(.*).py$')  { |m| code_changed(m[0]) }

def code_changed(file)
    #scrape
    run "python manage.py test scrape shelf"
end

def run(cmd)
    result = system("#{cmd}")
    growl result rescue nil
end

def growl(result)
  osn = Config::CONFIG["target_os"].downcase
  growlnotify = `which growlnotify`.chomp if osn.include?("darwin")
  growlnotify = `which notify-send`.chomp if osn.include?("linux")

  title = result ? "PASS" : "FAILURES"
    if title == "FAILURES"
        tag  = "<span background=\"darkred\">"
        info = "テストがこけました"
    else
        tag   = "<span background=\"darkgreen\">"
        info  = "テストは成功しています"
    end

  options = "-w -n Watchr --html '#{title}'  -m '#{info}'" if osn.include?("darwin")
  options = "-i '#{title}' '#{tag}<b>#{title}</b><br><br>#{info}</span>'" if osn.include?("linux")
  system %(#{growlnotify} #{options} &)
end
