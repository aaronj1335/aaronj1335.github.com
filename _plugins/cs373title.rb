require 'rubygems'
require 'andand'

module Jekyll
  module CS373TitleFilter
    def cs373title(input)
      in_semester = Date.today < Date.parse('2013-08-18')
      has_cs373_tag = @context.registers[:page]['tags'].andand.include? 'cs373'
      (has_cs373_tag and in_semester) ? "CS373: #{input}" : input
    end
  end
end

Liquid::Template.register_filter(Jekyll::CS373TitleFilter)
